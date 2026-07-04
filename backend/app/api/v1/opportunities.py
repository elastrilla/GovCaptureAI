from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.opportunity import Opportunity
from app.schemas.opportunity import OpportunityCreate, OpportunityRead


router = APIRouter(prefix="/opportunities", tags=["Opportunities"])


@router.post("/", response_model=OpportunityRead)
def create_opportunity(opportunity: OpportunityCreate, db: Session = Depends(get_db)):
    db_opportunity = Opportunity(
        sam_notice_id=opportunity.sam_notice_id,
        title=opportunity.title,
        solicitation_number=opportunity.solicitation_number,
        agency=opportunity.agency,
        naics_code=opportunity.naics_code,
        set_aside=opportunity.set_aside,
        posted_date=opportunity.posted_date,
        due_date=opportunity.due_date,
        status=opportunity.status,
        description=opportunity.description,
    )

    db.add(db_opportunity)
    db.commit()
    db.refresh(db_opportunity)

    return db_opportunity


@router.get("/", response_model=list[OpportunityRead])
def list_opportunities(db: Session = Depends(get_db)):
    return db.query(Opportunity).order_by(Opportunity.id).all()
