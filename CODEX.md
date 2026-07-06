# GovCaptureAI Codex Instructions

## Project Summary
GovCaptureAI is an AI-assisted government capture management platform for small businesses and government contractors.

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

## Next Planned Sprint
Sprint 6C — Save live SAM.gov search results into PostgreSQL.

Expected goal:
POST /api/v1/sam/search/save should work with SAM_API_MODE=live and save parsed SAM.gov results into the opportunities table while preventing duplicates.

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
