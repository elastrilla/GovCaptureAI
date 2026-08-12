# GovCaptureAI Codex Instructions

## Project Summary
GovCaptureAI is an AI-assisted government capture management platform for small businesses and government contractors.

## Product Vision Focus
The end objective is not just to pull opportunities from SAM.gov. GovCaptureAI should help a contractor:
- discover relevant opportunities
- qualify whether they should bid
- manage capture workflow and bid/no-bid decisions
- generate stronger proposal responses with AI support

Infrastructure work is important, but it only matters if it moves the product toward that contractor workflow.

## North Star Checklist
Before starting a sprint or feature, confirm:
- Does this make it easier to discover, qualify, manage, or respond to an opportunity?
- Does this strengthen the company-to-opportunity matching loop, not just raw data collection?
- Does this move the product closer to a usable contractor dashboard or workflow?
- Is this infrastructure in service of AI-assisted capture management, rather than becoming the end goal itself?
- After this work is done, will a user be closer to a bid/no-bid or proposal outcome?

Current prioritization lens:
- SAM.gov ingestion is foundation, not the final value.
- Company profile, capability matching, AI scoring, rationale, and workflow support are the core product differentiators.
- Frontend/dashboard work should expose real contractor decisions, not just backend status.

## Current Stack
- Backend: FastAPI
- Database: PostgreSQL
- ORM: SQLAlchemy
- Migrations: Alembic
- API Docs: Swagger/OpenAPI
- SAM.gov integration: live API connection working
- Frontend: planned
- Deployment target: Raspberry Pi 5 with Docker later

## Current Working Backend
Run backend from:
backend/

Start commands:
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload

Swagger:
http://127.0.0.1:8000/docs

## Important Rules
- Never commit backend/.env
- Never expose or print SAM_API_KEY
- Always run backend commands from the backend folder
- Use feature branches for new work
- Commit after each working milestone
- Keep changes small and testable
- Update the roadmap workbook after each sprint milestone

## Current Completed Milestones
- FastAPI backend foundation
- PostgreSQL database connection
- Alembic migrations
- Company and Opportunity API routes
- Mock SAM.gov search
- Save mock search results to PostgreSQL
- Opportunity status workflow
- Opportunity qualification score endpoint
- Opportunity dashboard summary endpoint
- Live SAM.gov API connection test
- Live SAM.gov search parser
- Company profile and capability fields
- Company profile update workflow
- Company knowledge library document inputs
- Automatic qualification score endpoint
- Qualification recommendation and rationale workflow
- Dashboard UI foundation for qualification decisions
- Opportunity list and detail review UI
- Workflow UI for status and qualification updates
- Notice type capture and filtering for RFI, RFQ, RFP, and Sources Sought opportunities
- Draft proposal response generator using opportunity, company, qualification, and document inputs
- Proposal review workflow with persisted drafts, readiness score, review status, notes, and gaps
- Docker deployment preparation for backend, frontend, and PostgreSQL demo services
- Raspberry Pi demo server runbook and helper scripts for sync, deploy, and health verification
- Client-facing sales package with product one-pager, demo script, and buyer FAQ
- Proposal export workflow with text download endpoint, dashboard export button, and API coverage
- Client-facing demo deck for buyer meetings and pilot conversations
- Pricing model and buyer-facing pricing brief for discovery, pilot, and implementation packaging
- Live demo polish with visible frontend source, API target, data mode, build version, and stale Raspberry Pi frontend verification
- Marketing plan, outreach templates, and demo prospect pipeline workbook for lining up buyer feedback conversations

## Next Planned Sprint
Sprint 13A — Pilot feedback loop, after demo pipeline readiness gates are met.

Expected goal:
Use real demo conversations to identify repeated buyer pains, objections, pilot candidates, and product gaps.

Before starting Sprint 13A, work the Sprint 12C demo pipeline until these readiness gates are met:
- at least 3 completed demos
- at least 5 logged feedback items
- at least 1 serious pilot candidate or referral path
- repeated pains or objections captured in the demo feedback tracker

## Roadmap Workbook
Roadmap file:
docs/ProjectManagement/GovCaptureAI_Roadmap.xlsx

Enhance it with:
- Dashboard tab
- Overall completion percentage
- Completed vs planned milestone chart
- Progress by workstream chart
- Sprint tracker
- Demo readiness checklist
- Risks and decisions log
