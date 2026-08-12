# GovCaptureAI

AI-powered Capture Management Platform for Government Contractors

## Vision

Help government contractors discover, qualify, manage, and respond to federal opportunities using Artificial Intelligence.

## North Star

GovCaptureAI is not just a SAM.gov integration project. The product should help a contractor move from opportunity discovery to bid/no-bid judgment to proposal execution with better speed and confidence.

When choosing what to build next, favor work that improves:
- opportunity relevance and discovery
- company capability matching
- AI qualification and rationale
- capture workflow visibility
- proposal readiness

## Technology Stack

- FastAPI
- Static HTML/CSS/JavaScript dashboard
- PostgreSQL
- Docker
- OpenAI GPT
- SAM.gov API

## Local Backend

```bash
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload
```

API docs:

```text
http://127.0.0.1:8000/docs
```

## Docker Demo

Docker keeps the backend on port `8000` and serves the static dashboard on port `8001`.
The Docker database is exposed on host port `5433` so it does not collide with a local PostgreSQL running on `5432`.

Recommended baseline:

```text
Docker Engine 20.x or newer
Docker Compose v2, or a recent docker-compose v1
```

If `docker-compose up --build` fails with `missing signature key`, Docker is too old to pull the current official base images. Update Docker Desktop first.

If the Mac cannot run a modern Docker version, use the Raspberry Pi 5 as the Docker host instead:

[Raspberry Pi 5 Docker Demo](docs/Deployment/RaspberryPi_Docker.md)

For the repeatable demo-server workflow:

[Demo Server Runbook](docs/Deployment/Demo_Server_Runbook.md)

Before a buyer walkthrough, run the demo-server check and confirm the dashboard sidebar shows the expected Demo environment, API target, data mode, and frontend version.

For client-facing positioning and demo support:

[GovCaptureAI One-Pager](docs/Sales/GovCaptureAI_One_Pager.md)

[GovCaptureAI Demo Script](docs/Sales/GovCaptureAI_Demo_Script.md)

[GovCaptureAI Marketing Plan](docs/Sales/GovCaptureAI_Marketing_Plan.md)

[GovCaptureAI Demo Outreach](docs/Sales/GovCaptureAI_Demo_Outreach.md)

[GovCaptureAI Demo Prospect Pipeline](docs/Sales/GovCaptureAI_Demo_Prospect_Pipeline.xlsx)

[GovCaptureAI Buyer FAQ](docs/Sales/GovCaptureAI_Buyer_FAQ.md)

[GovCaptureAI Demo Deck](docs/Sales/GovCaptureAI_Demo_Deck.pptx)

[GovCaptureAI Pricing Brief](docs/Sales/GovCaptureAI_Pricing_Brief.md)

[GovCaptureAI Pricing Model](docs/Sales/GovCaptureAI_Pricing_Model.xlsx)

## Proposal Export

Generated proposal drafts can be exported from the dashboard as a shareable text package. The export includes opportunity metadata, review status, readiness score, review notes, compliance notes, review gaps, and the draft response.

API route:

```text
GET /api/v1/opportunities/{opportunity_id}/proposal/{proposal_id}/export
```

Optional preflight:

```bash
./scripts/check-docker.sh
```

```bash
docker-compose up --build
```

Then open:

```text
Backend API: http://127.0.0.1:8000/docs
Dashboard:   http://127.0.0.1:8001
```

The backend container waits for PostgreSQL and runs `alembic upgrade head` at startup.

To stop the demo:

```bash
docker-compose down
```

To reset Docker database data:

```bash
docker-compose down -v
```

Do not commit `backend/.env`. Use `backend/.env.example` as the safe template.
