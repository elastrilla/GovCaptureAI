import asyncio
from datetime import date
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.api.v1.sam import _parse_sam_date, _save_sam_search_results
from app.sam.client import parse_sam_opportunity, search_sam_live
from app.sam.service import search_sam_mock
from app.database.base import Base
from app.core.config import settings
from app.models.opportunity import Opportunity
from app.schemas.sam import SamSearchRequest
from app.schemas.sam import SamOpportunityResult, SamSearchResponse


class FakeQuery:
    def __init__(self, existing_ids):
        self.existing_ids = existing_ids
        self.current_notice_id = None

    def filter(self, condition):
        self.current_notice_id = getattr(getattr(condition, "right", None), "value", None)
        return self

    def first(self):
        if self.current_notice_id in self.existing_ids:
            return object()
        return None


class FakeTransaction:
    def __init__(self, session):
        self.session = session

    def __enter__(self):
        self.session.begin_calls += 1
        return self.session

    def __exit__(self, exc_type, exc, tb):
        return False


class FakeSession:
    def __init__(self, existing_ids=None):
        self.existing_ids = set(existing_ids or [])
        self.added = []
        self.begin_calls = 0
        self.commit_calls = 0
        self.flush_calls = 0

    def begin(self):
        return FakeTransaction(self)

    def query(self, model):
        return FakeQuery(self.existing_ids)

    def add(self, obj):
        obj.id = len(self.added) + 1
        self.added.append(obj)

    def flush(self):
        self.flush_calls += 1

    def commit(self):
        self.commit_calls += 1


class SaveSamSearchResultsTests(unittest.TestCase):
    def test_parse_sam_date_handles_common_formats(self):
        self.assertEqual(_parse_sam_date("07/04/2026"), date(2026, 7, 4))
        self.assertEqual(_parse_sam_date("2026-07-04T10:30:00Z"), date(2026, 7, 4))
        self.assertIsNone(_parse_sam_date("not-a-date"))

    def test_save_sam_search_results_is_atomic_and_skips_duplicates(self):
        session = FakeSession(existing_ids={"EXISTING-001"})
        response = SamSearchResponse(
            source="sam_gov_live",
            count=2,
            results=[
                SamOpportunityResult(
                    sam_notice_id="EXISTING-001",
                    title="Existing Opportunity",
                    solicitation_number="RFP-001",
                    agency="Agency A",
                    naics_code="541512",
                    set_aside="Small Business",
                    posted_date="07/01/2026",
                    due_date="2026-08-01T00:00:00Z",
                    description="Already saved",
                ),
                SamOpportunityResult(
                    sam_notice_id="NEW-001",
                    title="New Opportunity",
                    solicitation_number="RFP-002",
                    agency="Agency B",
                    naics_code="541513",
                    set_aside="SDVOSB",
                    posted_date="07/02/2026",
                    due_date="2026-08-02T00:00:00Z",
                    summary="Fresh short summary",
                    description="Fresh import",
                ),
            ],
        )

        result = _save_sam_search_results(session, response)

        self.assertEqual(result["source"], "sam_gov_live")
        self.assertEqual(result["matched_count"], 2)
        self.assertEqual(result["saved_count"], 1)
        self.assertEqual(result["skipped_existing_count"], 1)
        self.assertEqual(len(result["saved_opportunities"]), 1)
        self.assertEqual(result["saved_opportunities"][0]["sam_notice_id"], "NEW-001")
        self.assertEqual(session.begin_calls, 1)
        self.assertEqual(session.commit_calls, 0)
        self.assertEqual(session.flush_calls, 1)
        self.assertEqual(len(session.added), 1)
        self.assertEqual(session.added[0].summary, "Fresh short summary")
        self.assertEqual(session.added[0].posted_date, date(2026, 7, 2))
        self.assertEqual(session.added[0].due_date, date(2026, 8, 2))


class SamClientMappingTests(unittest.TestCase):
    def test_search_sam_mock_filters_notice_type(self):
        result = search_sam_mock(SamSearchRequest(notice_type="rfq"))

        self.assertEqual(result.source, "mock_sam_service")
        self.assertEqual(result.count, 1)
        self.assertEqual(result.results[0].notice_type, "RFQ")

    def test_parse_sam_opportunity_infers_notice_type_from_solicitation(self):
        result = parse_sam_opportunity(
            {
                "noticeId": "INFER-001",
                "title": "Cloud Support",
                "solicitationNumber": "RFQ-2026-99",
            }
        )

        self.assertEqual(result.notice_type, "RFQ")

    def test_parse_sam_opportunity_maps_live_field_variants(self):
        item = {
            "id": "ALT-001",
            "opportunityTitle": "Cloud Modernization Support",
            "solicitation": {"number": "SOL-2026-15"},
            "notice": {"type": "Sources Sought"},
            "organizationHierarchy": {
                "topLevelAgency": {"name": "Department of Energy"},
            },
            "classification": {
                "naics": {"code": "541512"},
            },
            "typeOfSetAside": {"description": "Small Business"},
            "dates": {
                "posted": "2026-07-01",
                "responseDeadline": "2026-08-01T00:00:00Z",
            },
            "links": {
                "details": "https://sam.gov/opp/ALT-001",
            },
        }

        result = parse_sam_opportunity(item)

        self.assertEqual(result.sam_notice_id, "ALT-001")
        self.assertEqual(result.title, "Cloud Modernization Support")
        self.assertEqual(result.solicitation_number, "SOL-2026-15")
        self.assertEqual(result.notice_type, "Sources Sought")
        self.assertEqual(result.agency, "Department of Energy")
        self.assertEqual(result.naics_code, "541512")
        self.assertEqual(result.set_aside, "Small Business")
        self.assertEqual(result.posted_date, "2026-07-01")
        self.assertEqual(result.due_date, "2026-08-01T00:00:00Z")
        self.assertEqual(result.description, "https://sam.gov/opp/ALT-001")
        self.assertEqual(
            result.summary,
            "Sources Sought opportunity for Cloud Modernization Support from Department of Energy.",
        )

    @patch("app.sam.client.requests.get")
    @patch("app.sam.client.settings")
    def test_search_sam_live_reads_alternate_result_container_and_filters_agency(
        self,
        mock_settings,
        mock_get,
    ):
        mock_settings.SAM_API_KEY = "test-key"
        mock_settings.SAM_API_BASE_URL = "https://example.test/sam"

        mock_response = Mock()
        mock_response.json.return_value = {
            "results": [
                {
                    "noticeId": "ONE-001",
                    "title": "Energy Audit Support",
                    "noticeType": "Sources Sought",
                    "organizationHierarchy": {
                        "department": {"name": "Department of Energy"},
                    },
                },
                {
                    "noticeId": "TWO-002",
                    "title": "Logistics Support",
                    "noticeType": "RFQ",
                    "organizationHierarchy": {
                        "department": {"name": "Department of Transportation"},
                    },
                },
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = search_sam_live(
            SamSearchRequest(
                keyword="support",
                agency="energy",
                notice_type="sources",
                limit=5,
                posted_from="07/01/2026",
                posted_to="07/31/2026",
            )
        )

        self.assertEqual(result.source, "sam_gov_live")
        self.assertEqual(result.count, 1)
        self.assertEqual(result.results[0].sam_notice_id, "ONE-001")
        self.assertEqual(result.results[0].agency, "Department of Energy")
        self.assertEqual(result.results[0].notice_type, "Sources Sought")
        mock_get.assert_called_once()
        self.assertEqual(mock_get.call_args.kwargs["params"]["title"], "support")
        self.assertEqual(mock_get.call_args.kwargs["params"]["postedFrom"], "07/01/2026")
        self.assertEqual(mock_get.call_args.kwargs["params"]["postedTo"], "07/31/2026")


def _date_string(value):
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return value


async def _call_asgi_json(app, method, path, payload):
    body = json.dumps(payload).encode("utf-8")
    messages = []
    receive_called = False

    async def receive():
        nonlocal receive_called
        if receive_called:
            return {"type": "http.disconnect"}

        receive_called = True
        return {
            "type": "http.request",
            "body": body,
            "more_body": False,
        }

    async def send(message):
        messages.append(message)

    scope = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": method,
        "scheme": "http",
        "path": path,
        "raw_path": path.encode("utf-8"),
        "query_string": b"",
        "headers": [
            (b"host", b"testserver"),
            (b"content-type", b"application/json"),
            (b"content-length", str(len(body)).encode("ascii")),
        ],
        "client": ("testclient", 50000),
        "server": ("testserver", 80),
    }

    await app(scope, receive, send)

    status_code = None
    response_headers = []
    response_body = b""

    for message in messages:
        if message["type"] == "http.response.start":
            status_code = message["status"]
            response_headers = message.get("headers", [])
        elif message["type"] == "http.response.body":
            response_body += message.get("body", b"")

    return {
        "status_code": status_code,
        "headers": {
            key.decode("latin-1"): value.decode("latin-1")
            for key, value in response_headers
        },
        "body": response_body.decode("utf-8"),
    }


class TempSQLiteDatabase:
    def __init__(self):
        self._tmpdir = tempfile.TemporaryDirectory(prefix="govcaptureai_sqlite_")
        self.db_path = Path(self._tmpdir.name) / "test.db"
        self.engine = None
        self.SessionLocal = None

    def start(self):
        self.engine = create_engine(
            f"sqlite:///{self.db_path}",
            connect_args={"check_same_thread": False},
            future=True,
        )
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
            future=True,
        )
        Base.metadata.create_all(bind=self.engine)
        return self

    def stop(self):
        if self.engine is not None:
            self.engine.dispose()
        self._tmpdir.cleanup()

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()


class SamApiIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.database = TempSQLiteDatabase().start()

        import app.api.v1.sam as sam_module
        import app.main as main_module

        cls.sam_module = sam_module
        cls.main_module = main_module
        cls.app = main_module.app
        cls.app.dependency_overrides[sam_module.get_db] = cls.database.get_db

    @classmethod
    def tearDownClass(cls):
        cls.app.dependency_overrides.clear()
        cls.database.stop()

    def setUp(self):
        with self.database.engine.begin() as connection:
            connection.execute(text("DELETE FROM opportunities"))
            connection.execute(text("DELETE FROM companies"))
            connection.execute(text("DELETE FROM users"))

    def test_search_save_endpoint_persists_and_skips_duplicates(self):
        payload = {
            "keyword": "cloud",
            "limit": 5,
        }

        mock_response = SamSearchResponse(
            source="mock_sam_service",
            count=2,
            results=[
                SamOpportunityResult(
                    sam_notice_id="API-001",
                    title="Cloud Migration and Infrastructure Support",
                    solicitation_number="RFQ-001",
                    notice_type="RFQ",
                    agency="Department of Defense",
                    naics_code="541513",
                    set_aside="Small Business",
                    posted_date="07/01/2026",
                    due_date="2026-08-01T00:00:00Z",
                    summary="First import summary",
                    description="First import",
                ),
                SamOpportunityResult(
                    sam_notice_id="API-002",
                    title="Cloud Security Assessment",
                    solicitation_number="RFP-002",
                    notice_type="RFP",
                    agency="Department of Veterans Affairs",
                    naics_code="541512",
                    set_aside="SDVOSB",
                    posted_date="07/02/2026",
                    due_date="2026-08-02T00:00:00Z",
                    summary="Second import summary",
                    description="Second import",
                ),
            ],
        )

        with patch.object(self.sam_module, "search_sam_opportunities", return_value=mock_response):
            first = asyncio.run(
                _call_asgi_json(
                    self.app,
                    "POST",
                    "/api/v1/sam/search/save",
                    payload,
                )
            )
            second = asyncio.run(
                _call_asgi_json(
                    self.app,
                    "POST",
                    "/api/v1/sam/search/save",
                    payload,
                )
            )

        self.assertEqual(first["status_code"], 200)
        self.assertEqual(second["status_code"], 200)

        first_body = json.loads(first["body"])
        second_body = json.loads(second["body"])

        self.assertEqual(first_body["source"], "mock_sam_service")
        self.assertEqual(first_body["matched_count"], 2)
        self.assertEqual(first_body["saved_count"], 2)
        self.assertEqual(first_body["skipped_existing_count"], 0)
        self.assertEqual(len(first_body["saved_opportunities"]), 2)

        self.assertEqual(second_body["saved_count"], 0)
        self.assertEqual(second_body["skipped_existing_count"], 2)
        self.assertEqual(len(second_body["saved_opportunities"]), 0)

        with self.database.engine.connect() as connection:
            rows = connection.execute(
                text(
                    "SELECT sam_notice_id, title, notice_type, summary, posted_date, due_date, status "
                    "FROM opportunities ORDER BY id"
                )
            ).mappings().all()

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["sam_notice_id"], "API-001")
        self.assertEqual(rows[0]["notice_type"], "RFQ")
        self.assertEqual(rows[0]["summary"], "First import summary")
        self.assertEqual(_date_string(rows[0]["posted_date"]), "2026-07-01")
        self.assertEqual(_date_string(rows[0]["due_date"]), "2026-08-01")
        self.assertEqual(rows[0]["status"], "new")
        self.assertEqual(rows[1]["sam_notice_id"], "API-002")
        self.assertEqual(rows[1]["notice_type"], "RFP")
        self.assertEqual(_date_string(rows[1]["posted_date"]), "2026-07-02")
        self.assertEqual(_date_string(rows[1]["due_date"]), "2026-08-02")

    @patch("app.sam.client.requests.get")
    @patch("app.sam.client.settings")
    @patch("app.sam.service.settings")
    def test_search_save_endpoint_works_in_live_mode_and_skips_duplicates(
        self,
        mock_service_settings,
        mock_client_settings,
        mock_get,
    ):
        mock_service_settings.SAM_API_MODE = "live"
        mock_client_settings.SAM_API_KEY = "test-live-key"
        mock_client_settings.SAM_API_BASE_URL = "https://example.test/live"

        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "opportunitiesData": [
                {
                    "noticeId": "LIVE-001",
                    "title": "Live Cloud Infrastructure Support",
                    "solicitationNumber": "LIVE-RFQ-001",
                    "type": "RFQ",
                    "fullParentPathName": "Department of Defense",
                    "naicsCode": "541513",
                    "typeOfSetAsideDescription": "Small Business",
                    "postedDate": "07/03/2026",
                    "responseDeadline": "2026-08-03T00:00:00Z",
                    "description": "Support live cloud migration planning.",
                },
                {
                    "noticeId": "LIVE-002",
                    "opportunityTitle": "Live Cybersecurity Assessment",
                    "noticeType": "Sources Sought",
                    "organizationHierarchy": {
                        "department": {"name": "Department of Veterans Affairs"},
                    },
                    "classification": {
                        "naics": {"code": "541512"},
                    },
                    "typeOfSetAside": {"description": "SDVOSB"},
                    "dates": {
                        "posted": "2026-07-04",
                        "responseDeadline": "2026-08-04T00:00:00Z",
                    },
                    "links": {
                        "details": "https://sam.gov/opp/LIVE-002",
                    },
                },
            ],
        }
        mock_get.return_value = mock_response

        payload = {
            "keyword": "live",
            "limit": 10,
            "posted_from": "07/01/2026",
            "posted_to": "07/31/2026",
        }

        first = asyncio.run(
            _call_asgi_json(
                self.app,
                "POST",
                "/api/v1/sam/search/save",
                payload,
            )
        )
        second = asyncio.run(
            _call_asgi_json(
                self.app,
                "POST",
                "/api/v1/sam/search/save",
                payload,
            )
        )

        self.assertEqual(first["status_code"], 200)
        self.assertEqual(second["status_code"], 200)

        first_body = json.loads(first["body"])
        second_body = json.loads(second["body"])

        self.assertEqual(first_body["source"], "sam_gov_live")
        self.assertEqual(first_body["matched_count"], 2)
        self.assertEqual(first_body["saved_count"], 2)
        self.assertEqual(first_body["skipped_existing_count"], 0)

        self.assertEqual(second_body["source"], "sam_gov_live")
        self.assertEqual(second_body["saved_count"], 0)
        self.assertEqual(second_body["skipped_existing_count"], 2)

        self.assertEqual(mock_get.call_count, 2)
        first_params = mock_get.call_args.kwargs["params"]
        self.assertEqual(first_params["title"], "live")
        self.assertEqual(first_params["postedFrom"], "07/01/2026")
        self.assertEqual(first_params["postedTo"], "07/31/2026")

        with self.database.engine.connect() as connection:
            rows = connection.execute(
                text(
                    "SELECT sam_notice_id, title, notice_type, agency, naics_code, set_aside, summary, posted_date, due_date, status "
                    "FROM opportunities ORDER BY id"
                )
            ).mappings().all()

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["sam_notice_id"], "LIVE-001")
        self.assertEqual(rows[0]["notice_type"], "RFQ")
        self.assertEqual(rows[0]["agency"], "Department of Defense")
        self.assertEqual(rows[0]["naics_code"], "541513")
        self.assertEqual(rows[0]["set_aside"], "Small Business")
        self.assertEqual(rows[0]["summary"], "Support live cloud migration planning.")
        self.assertEqual(_date_string(rows[0]["posted_date"]), "2026-07-03")
        self.assertEqual(_date_string(rows[0]["due_date"]), "2026-08-03")
        self.assertEqual(rows[0]["status"], "new")

        self.assertEqual(rows[1]["sam_notice_id"], "LIVE-002")
        self.assertEqual(rows[1]["notice_type"], "Sources Sought")
        self.assertEqual(rows[1]["agency"], "Department of Veterans Affairs")
        self.assertEqual(rows[1]["naics_code"], "541512")
        self.assertEqual(rows[1]["set_aside"], "SDVOSB")
        self.assertEqual(
            rows[1]["summary"],
            "Sources Sought opportunity for Live Cybersecurity Assessment from Department of Veterans Affairs.",
        )
        self.assertEqual(_date_string(rows[1]["posted_date"]), "2026-07-04")
        self.assertEqual(_date_string(rows[1]["due_date"]), "2026-08-04")
        self.assertEqual(rows[1]["status"], "new")

    def test_demo_reset_deletes_opportunities_when_enabled(self):
        with self.database.SessionLocal() as session:
            session.add(
                Opportunity(
                    sam_notice_id="RESET-001",
                    title="Demo opportunity",
                    status="new",
                )
            )
            session.commit()

        with patch.object(settings, "DEMO_RESET_ENABLED", True):
            response = asyncio.run(
                _call_asgi_json(
                    self.app,
                    "POST",
                    "/api/v1/opportunities/demo/reset",
                    {},
                )
            )

        self.assertEqual(response["status_code"], 200)
        body = json.loads(response["body"])
        self.assertEqual(body["deleted_opportunities"], 1)
        self.assertEqual(body["deleted_proposals"], 0)


if __name__ == "__main__":
    unittest.main()
