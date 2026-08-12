import asyncio
import json
import tempfile
import unittest
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.database.base import Base
from app.models import Company, Document, Opportunity, Proposal, User


async def _call_asgi_json(app, method, path, payload=None):
    body = json.dumps(payload or {}).encode("utf-8")
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

    headers = [(b"host", b"testserver")]
    if payload is not None:
        headers.extend(
            [
                (b"content-type", b"application/json"),
                (b"content-length", str(len(body)).encode("ascii")),
            ]
        )

    scope = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": method,
        "scheme": "http",
        "path": path,
        "raw_path": path.encode("utf-8"),
        "query_string": b"",
        "headers": headers,
        "client": ("testclient", 50000),
        "server": ("testserver", 80),
    }

    await app(scope, receive, send)

    status_code = None
    response_body = b""
    response_headers = {}

    for message in messages:
        if message["type"] == "http.response.start":
            status_code = message["status"]
            response_headers = {
                key.decode("latin-1").lower(): value.decode("latin-1")
                for key, value in message.get("headers", [])
            }
        elif message["type"] == "http.response.body":
            response_body += message.get("body", b"")

    return {
        "status_code": status_code,
        "body": response_body.decode("utf-8"),
        "headers": response_headers,
    }


class TempSQLiteDatabase:
    def __init__(self):
        self._tmpdir = tempfile.TemporaryDirectory(prefix="govcaptureai_companies_")
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
        _ = (User, Company, Document, Opportunity, Proposal)
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


class CompanyApiIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.database = TempSQLiteDatabase().start()

        import app.api.v1.companies as companies_module
        import app.api.v1.opportunities as opportunities_module
        import app.main as main_module

        cls.companies_module = companies_module
        cls.opportunities_module = opportunities_module
        cls.app = main_module.app
        cls.app.dependency_overrides[companies_module.get_db] = cls.database.get_db
        cls.app.dependency_overrides[opportunities_module.get_db] = cls.database.get_db

    @classmethod
    def tearDownClass(cls):
        cls.app.dependency_overrides.clear()
        cls.database.stop()

    def setUp(self):
        with self.database.engine.begin() as connection:
            connection.execute(text("DELETE FROM proposals"))
            connection.execute(text("DELETE FROM documents"))
            connection.execute(text("DELETE FROM companies"))
            connection.execute(text("DELETE FROM opportunities"))
            connection.execute(text("DELETE FROM users"))

    def test_create_and_list_companies_with_profile_fields(self):
        create_payload = {
            "name": "Apex Capture Group",
            "website": "https://apex.example",
            "description": "Federal IT and cybersecurity contractor.",
            "core_capabilities": "Cloud engineering, cybersecurity, help desk.",
            "differentiators": "Fast transition teams and cleared staff.",
            "certifications": "8(a); HUBZone; ISO 9001",
            "target_naics_codes": "541512,541519,561210",
            "target_agencies": "Department of Energy; VA",
            "past_performance_summary": "Supported 12 federal modernization efforts.",
        }

        create_response = asyncio.run(
            _call_asgi_json(
                self.app,
                "POST",
                "/api/v1/companies/",
                create_payload,
            )
        )
        list_response = asyncio.run(
            _call_asgi_json(
                self.app,
                "GET",
                "/api/v1/companies/",
            )
        )

        self.assertEqual(create_response["status_code"], 200)
        self.assertEqual(list_response["status_code"], 200)

        created_company = json.loads(create_response["body"])
        listed_companies = json.loads(list_response["body"])

        self.assertEqual(created_company["name"], "Apex Capture Group")
        self.assertEqual(created_company["core_capabilities"], create_payload["core_capabilities"])
        self.assertEqual(created_company["certifications"], create_payload["certifications"])
        self.assertEqual(created_company["target_naics_codes"], create_payload["target_naics_codes"])
        self.assertEqual(len(listed_companies), 1)
        self.assertEqual(listed_companies[0]["past_performance_summary"], create_payload["past_performance_summary"])

    def test_patch_company_updates_qualification_profile(self):
        create_payload = {
            "name": "Signal Ridge Consulting",
        }

        create_response = asyncio.run(
            _call_asgi_json(
                self.app,
                "POST",
                "/api/v1/companies/",
                create_payload,
            )
        )
        created_company = json.loads(create_response["body"])

        patch_payload = {
            "core_capabilities": "Acquisition support and program management.",
            "target_agencies": "USAF; DHS",
            "past_performance_summary": "Led recompete capture strategy for two task orders.",
        }

        patch_response = asyncio.run(
            _call_asgi_json(
                self.app,
                "PATCH",
                f"/api/v1/companies/{created_company['id']}",
                patch_payload,
            )
        )
        get_response = asyncio.run(
            _call_asgi_json(
                self.app,
                "GET",
                f"/api/v1/companies/{created_company['id']}",
            )
        )

        self.assertEqual(patch_response["status_code"], 200)
        self.assertEqual(get_response["status_code"], 200)

        updated_company = json.loads(patch_response["body"])
        fetched_company = json.loads(get_response["body"])

        self.assertEqual(updated_company["core_capabilities"], patch_payload["core_capabilities"])
        self.assertEqual(updated_company["target_agencies"], patch_payload["target_agencies"])
        self.assertEqual(fetched_company["past_performance_summary"], patch_payload["past_performance_summary"])

        with self.database.engine.connect() as connection:
            row = connection.execute(
                text(
                    "SELECT core_capabilities, target_agencies, past_performance_summary "
                    "FROM companies WHERE id = :company_id"
                ),
                {"company_id": created_company["id"]},
            ).mappings().one()

        self.assertEqual(row["core_capabilities"], patch_payload["core_capabilities"])
        self.assertEqual(row["target_agencies"], patch_payload["target_agencies"])
        self.assertEqual(
            row["past_performance_summary"],
            patch_payload["past_performance_summary"],
        )

    def test_company_documents_store_qualification_evidence(self):
        create_company_response = asyncio.run(
            _call_asgi_json(
                self.app,
                "POST",
                "/api/v1/companies/",
                {"name": "Northwind Federal"},
            )
        )
        company = json.loads(create_company_response["body"])

        document_payload = {
            "document_type": "capability_statement",
            "title": "Capability Statement 2026",
            "filename": "northwind-capability-statement.pdf",
            "content_text": "Core capabilities include cloud modernization and zero trust support.",
            "notes": "Use for civilian agency pursuits first.",
        }

        create_document_response = asyncio.run(
            _call_asgi_json(
                self.app,
                "POST",
                f"/api/v1/companies/{company['id']}/documents",
                document_payload,
            )
        )
        list_documents_response = asyncio.run(
            _call_asgi_json(
                self.app,
                "GET",
                f"/api/v1/companies/{company['id']}/documents",
            )
        )

        self.assertEqual(create_document_response["status_code"], 200)
        self.assertEqual(list_documents_response["status_code"], 200)

        created_document = json.loads(create_document_response["body"])
        listed_documents = json.loads(list_documents_response["body"])

        self.assertEqual(created_document["company_id"], company["id"])
        self.assertEqual(created_document["document_type"], document_payload["document_type"])
        self.assertEqual(created_document["filename"], document_payload["filename"])
        self.assertEqual(len(listed_documents), 1)
        self.assertEqual(listed_documents[0]["content_text"], document_payload["content_text"])
        self.assertEqual(listed_documents[0]["notes"], document_payload["notes"])

        get_document_response = asyncio.run(
            _call_asgi_json(
                self.app,
                "GET",
                f"/api/v1/companies/{company['id']}/documents/{created_document['id']}",
            )
        )

        self.assertEqual(get_document_response["status_code"], 200)
        fetched_document = json.loads(get_document_response["body"])
        self.assertEqual(fetched_document["title"], document_payload["title"])

        with self.database.engine.connect() as connection:
            row = connection.execute(
                text(
                    "SELECT company_id, document_type, filename, content_text, notes "
                    "FROM documents WHERE id = :document_id"
                ),
                {"document_id": created_document["id"]},
            ).mappings().one()

        self.assertEqual(row["company_id"], company["id"])
        self.assertEqual(row["document_type"], document_payload["document_type"])
        self.assertEqual(row["filename"], document_payload["filename"])
        self.assertEqual(row["content_text"], document_payload["content_text"])
        self.assertEqual(row["notes"], document_payload["notes"])

    def test_auto_scores_opportunity_from_company_fit_and_documents(self):
        company_response = asyncio.run(
            _call_asgi_json(
                self.app,
                "POST",
                "/api/v1/companies/",
                {
                    "name": "Blue Harbor Systems",
                    "core_capabilities": "Cloud modernization, zero trust, cybersecurity engineering.",
                    "certifications": "8(a); HUBZone; Small Business",
                    "target_naics_codes": "541512,541519",
                    "target_agencies": "Department of Energy; VA",
                    "past_performance_summary": "Delivered zero trust modernization for a civilian agency.",
                },
            )
        )
        company = json.loads(company_response["body"])

        asyncio.run(
            _call_asgi_json(
                self.app,
                "POST",
                f"/api/v1/companies/{company['id']}/documents",
                {
                    "document_type": "capability_statement",
                    "title": "Zero Trust Capability Statement",
                    "content_text": "Blue Harbor delivers cloud modernization and zero trust architecture support.",
                    "notes": "Strong fit for DOE modernization work.",
                },
            )
        )
        asyncio.run(
            _call_asgi_json(
                self.app,
                "POST",
                f"/api/v1/companies/{company['id']}/documents",
                {
                    "document_type": "past_performance",
                    "title": "Civilian Zero Trust Program",
                    "content_text": "Past performance includes cybersecurity engineering and cloud migration.",
                },
            )
        )

        opportunity_response = asyncio.run(
            _call_asgi_json(
                self.app,
                "POST",
                "/api/v1/opportunities/",
                {
                    "title": "Zero Trust Cloud Modernization Support",
                    "notice_type": "RFP",
                    "agency": "Department of Energy",
                    "naics_code": "541512",
                    "set_aside": "8(a)",
                    "description": "Seeking cybersecurity engineering and cloud modernization support.",
                },
            )
        )
        opportunity = json.loads(opportunity_response["body"])
        self.assertEqual(opportunity["notice_type"], "RFP")

        auto_score_response = asyncio.run(
            _call_asgi_json(
                self.app,
                "POST",
                f"/api/v1/opportunities/{opportunity['id']}/score/auto",
                {"company_id": company["id"]},
            )
        )

        self.assertEqual(auto_score_response["status_code"], 200)

        scored_opportunity = json.loads(auto_score_response["body"])
        self.assertGreaterEqual(scored_opportunity["qualification_score"], 8)
        self.assertEqual(scored_opportunity["qualification_recommendation"], "pursue")
        self.assertIn("Recommendation: Pursue", scored_opportunity["qualification_rationale"])
        self.assertIn("Strengths:", scored_opportunity["qualification_rationale"])
        self.assertIn("NAICS match", scored_opportunity["qualification_rationale"])
        self.assertIn("agency match", scored_opportunity["qualification_rationale"])
        self.assertIn("set-aside alignment", scored_opportunity["qualification_rationale"])
        self.assertIn("capability overlap", scored_opportunity["qualification_rationale"])

        with self.database.engine.connect() as connection:
            row = connection.execute(
                text(
                    "SELECT qualification_score, qualification_recommendation, qualification_rationale "
                    "FROM opportunities WHERE id = :opportunity_id"
                ),
                {"opportunity_id": opportunity["id"]},
            ).mappings().one()

        self.assertGreaterEqual(row["qualification_score"], 8)
        self.assertEqual(row["qualification_recommendation"], "pursue")
        self.assertIn("past performance evidence", row["qualification_rationale"])

    def test_auto_score_surfaces_review_gaps_for_weaker_fit(self):
        company_response = asyncio.run(
            _call_asgi_json(
                self.app,
                "POST",
                "/api/v1/companies/",
                {
                    "name": "Harbor Admin Services",
                    "target_naics_codes": "561110",
                    "target_agencies": "GSA",
                },
            )
        )
        company = json.loads(company_response["body"])

        opportunity_response = asyncio.run(
            _call_asgi_json(
                self.app,
                "POST",
                "/api/v1/opportunities/",
                {
                    "title": "Space Systems Engineering Support",
                    "agency": "NASA",
                    "naics_code": "541330",
                    "set_aside": "HUBZone",
                    "description": "Engineering support for mission systems integration.",
                },
            )
        )
        opportunity = json.loads(opportunity_response["body"])

        auto_score_response = asyncio.run(
            _call_asgi_json(
                self.app,
                "POST",
                f"/api/v1/opportunities/{opportunity['id']}/score/auto",
                {"company_id": company["id"]},
            )
        )

        self.assertEqual(auto_score_response["status_code"], 200)

        scored_opportunity = json.loads(auto_score_response["body"])
        self.assertLessEqual(scored_opportunity["qualification_score"], 4)
        self.assertEqual(scored_opportunity["qualification_recommendation"], "no_bid")
        self.assertIn("Recommendation: No-bid", scored_opportunity["qualification_rationale"])
        self.assertIn("Gaps to Review:", scored_opportunity["qualification_rationale"])
        self.assertIn("no target NAICS match", scored_opportunity["qualification_rationale"])
        self.assertIn("target agency coverage is not yet clear", scored_opportunity["qualification_rationale"])

    def test_draft_proposal_response_uses_capture_inputs_and_sets_drafting_status(self):
        company_response = asyncio.run(
            _call_asgi_json(
                self.app,
                "POST",
                "/api/v1/companies/",
                {
                    "name": "Blue Harbor Systems",
                    "core_capabilities": "Cloud modernization, zero trust, cybersecurity engineering.",
                    "differentiators": "Cleared transition team and repeatable delivery controls.",
                    "certifications": "8(a); Small Business",
                    "past_performance_summary": "Delivered zero trust modernization for a civilian agency.",
                },
            )
        )
        company = json.loads(company_response["body"])

        asyncio.run(
            _call_asgi_json(
                self.app,
                "POST",
                f"/api/v1/companies/{company['id']}/documents",
                {
                    "document_type": "past_performance",
                    "title": "Civilian Zero Trust Program",
                    "content_text": "Past performance includes cybersecurity engineering and cloud migration.",
                },
            )
        )

        opportunity_response = asyncio.run(
            _call_asgi_json(
                self.app,
                "POST",
                "/api/v1/opportunities/",
                {
                    "title": "Zero Trust Cloud Modernization Support",
                    "notice_type": "RFP",
                    "agency": "Department of Energy",
                    "naics_code": "541512",
                    "set_aside": "8(a)",
                    "description": "Seeking cybersecurity engineering and cloud modernization support.",
                },
            )
        )
        opportunity = json.loads(opportunity_response["body"])

        asyncio.run(
            _call_asgi_json(
                self.app,
                "POST",
                f"/api/v1/opportunities/{opportunity['id']}/score",
                {
                    "score": 9,
                    "recommendation": "pursue",
                    "rationale": (
                        "Recommendation: Pursue.\n\n"
                        "Strengths: NAICS match; agency match; capability overlap.\n\n"
                        "Gaps to Review: confirm pricing history."
                    ),
                },
            )
        )

        draft_response = asyncio.run(
            _call_asgi_json(
                self.app,
                "POST",
                f"/api/v1/opportunities/{opportunity['id']}/proposal/draft",
                {
                    "company_id": company["id"],
                    "instructions": "Emphasize transition speed.",
                },
            )
        )

        self.assertEqual(draft_response["status_code"], 200)

        draft = json.loads(draft_response["body"])
        self.assertIsInstance(draft["id"], int)
        self.assertEqual(draft["opportunity_id"], opportunity["id"])
        self.assertEqual(draft["company_id"], company["id"])
        self.assertEqual(draft["review_status"], "draft_generated")
        self.assertEqual(draft["readiness_score"], 30)
        self.assertIn("Draft Response", draft["title"])
        self.assertIn("Blue Harbor Systems", draft["executive_summary"])
        self.assertIn("Zero Trust Cloud Modernization Support", draft["title"])
        self.assertIn("Civilian Zero Trust Program", draft["past_performance"])
        self.assertIn("Compliance Notes", draft["draft_text"])
        self.assertIn("Review Gaps", draft["draft_text"])
        self.assertIn("Emphasize transition speed", " ".join(draft["compliance_notes"]))

        with self.database.engine.connect() as connection:
            row = connection.execute(
                text(
                    "SELECT status FROM opportunities WHERE id = :opportunity_id"
                ),
                {"opportunity_id": opportunity["id"]},
            ).mappings().one()
            proposal_row = connection.execute(
                text(
                    "SELECT review_status, readiness_score, review_gaps "
                    "FROM proposals WHERE id = :proposal_id"
                ),
                {"proposal_id": draft["id"]},
            ).mappings().one()

        self.assertEqual(row["status"], "drafting")
        self.assertEqual(proposal_row["review_status"], "draft_generated")
        self.assertEqual(proposal_row["readiness_score"], 30)
        self.assertIn("confirm pricing history", proposal_row["review_gaps"])

    def test_proposal_review_workflow_updates_readiness_and_latest_draft(self):
        company_response = asyncio.run(
            _call_asgi_json(
                self.app,
                "POST",
                "/api/v1/companies/",
                {
                    "name": "Review Ready Federal",
                    "core_capabilities": "Proposal operations and cloud delivery.",
                },
            )
        )
        company = json.loads(company_response["body"])

        opportunity_response = asyncio.run(
            _call_asgi_json(
                self.app,
                "POST",
                "/api/v1/opportunities/",
                {
                    "title": "Cloud Help Desk Support",
                    "notice_type": "RFQ",
                    "agency": "GSA",
                    "description": "Help desk and cloud operations support.",
                },
            )
        )
        opportunity = json.loads(opportunity_response["body"])

        draft_response = asyncio.run(
            _call_asgi_json(
                self.app,
                "POST",
                f"/api/v1/opportunities/{opportunity['id']}/proposal/draft",
                {"company_id": company["id"]},
            )
        )
        draft = json.loads(draft_response["body"])

        review_response = asyncio.run(
            _call_asgi_json(
                self.app,
                "PATCH",
                f"/api/v1/opportunities/{opportunity['id']}/proposal/{draft['id']}/review",
                {
                    "review_status": "ready_for_final",
                    "readiness_score": 88,
                    "review_notes": "Ready after pricing and compliance check.",
                    "review_gaps": ["Confirm price volume", "Add final QA sign-off"],
                },
            )
        )
        latest_response = asyncio.run(
            _call_asgi_json(
                self.app,
                "GET",
                f"/api/v1/opportunities/{opportunity['id']}/proposal/latest",
            )
        )

        self.assertEqual(review_response["status_code"], 200)
        self.assertEqual(latest_response["status_code"], 200)

        reviewed = json.loads(review_response["body"])
        latest = json.loads(latest_response["body"])

        self.assertEqual(reviewed["review_status"], "ready_for_final")
        self.assertEqual(reviewed["readiness_score"], 88)
        self.assertEqual(reviewed["review_notes"], "Ready after pricing and compliance check.")
        self.assertEqual(reviewed["review_gaps"], ["Confirm price volume", "Add final QA sign-off"])
        self.assertEqual(latest["id"], draft["id"])
        self.assertEqual(latest["readiness_score"], 88)

    def test_proposal_export_returns_shareable_text_attachment(self):
        company_response = asyncio.run(
            _call_asgi_json(
                self.app,
                "POST",
                "/api/v1/companies/",
                {
                    "name": "Export Ready LLC",
                    "core_capabilities": "Proposal writing and capture operations.",
                    "differentiators": "Senior review bench and compliance discipline.",
                },
            )
        )
        company = json.loads(company_response["body"])

        opportunity_response = asyncio.run(
            _call_asgi_json(
                self.app,
                "POST",
                "/api/v1/opportunities/",
                {
                    "title": "Proposal Export Pilot",
                    "notice_type": "RFP",
                    "agency": "NASA",
                    "solicitation_number": "80NSSC-EXPORT",
                    "naics_code": "541611",
                    "description": "Capture and proposal support services.",
                },
            )
        )
        opportunity = json.loads(opportunity_response["body"])

        draft_response = asyncio.run(
            _call_asgi_json(
                self.app,
                "POST",
                f"/api/v1/opportunities/{opportunity['id']}/proposal/draft",
                {"company_id": company["id"]},
            )
        )
        draft = json.loads(draft_response["body"])

        review_response = asyncio.run(
            _call_asgi_json(
                self.app,
                "PATCH",
                f"/api/v1/opportunities/{opportunity['id']}/proposal/{draft['id']}/review",
                {
                    "review_status": "ready_for_final",
                    "readiness_score": 91,
                    "review_notes": "Export package ready for capture lead.",
                    "review_gaps": ["Confirm pricing attachment"],
                },
            )
        )
        export_response = asyncio.run(
            _call_asgi_json(
                self.app,
                "GET",
                f"/api/v1/opportunities/{opportunity['id']}/proposal/{draft['id']}/export",
            )
        )

        self.assertEqual(review_response["status_code"], 200)
        self.assertEqual(export_response["status_code"], 200)
        self.assertIn("text/plain", export_response["headers"]["content-type"])
        self.assertIn(
            "proposal-export-pilot-proposal-export.txt",
            export_response["headers"]["content-disposition"],
        )
        self.assertIn("GovCaptureAI Proposal Export", export_response["body"])
        self.assertIn("Proposal Export Pilot", export_response["body"])
        self.assertIn("Export Ready LLC", export_response["body"])
        self.assertIn("Readiness Score: 91/100", export_response["body"])
        self.assertIn("Confirm pricing attachment", export_response["body"])
        self.assertIn("Draft Response", export_response["body"])


if __name__ == "__main__":
    unittest.main()
