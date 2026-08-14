from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.company import Company
from app.models.document import Document
from app.schemas.company import CompanyCreate, CompanyRead, CompanyUpdate
from app.schemas.document import DocumentCreate, DocumentRead


router = APIRouter(prefix="/companies", tags=["Companies"])


@router.post("/", response_model=CompanyRead)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    db_company = Company(
        name=company.name,
        website=company.website,
        description=company.description,
        core_capabilities=company.core_capabilities,
        differentiators=company.differentiators,
        certifications=company.certifications,
        target_naics_codes=company.target_naics_codes,
        target_agencies=company.target_agencies,
        past_performance_summary=company.past_performance_summary,
    )

    db.add(db_company)
    db.commit()
    db.refresh(db_company)

    return db_company


@router.get("/", response_model=list[CompanyRead])
def list_companies(db: Session = Depends(get_db)):
    return db.query(Company).order_by(Company.id).all()


@router.get("/{company_id}", response_model=CompanyRead)
def get_company(company_id: int, db: Session = Depends(get_db)):
    company = (
        db.query(Company)
        .filter(Company.id == company_id)
        .first()
    )

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    return company


@router.patch("/{company_id}", response_model=CompanyRead)
def update_company(
    company_id: int,
    company_update: CompanyUpdate,
    db: Session = Depends(get_db),
):
    company = (
        db.query(Company)
        .filter(Company.id == company_id)
        .first()
    )

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    for field, value in company_update.model_dump(exclude_unset=True).items():
        setattr(company, field, value)

    db.commit()
    db.refresh(company)

    return company


@router.post("/{company_id}/documents", response_model=DocumentRead)
def create_company_document(
    company_id: int,
    document: DocumentCreate,
    db: Session = Depends(get_db),
):
    company = (
        db.query(Company)
        .filter(Company.id == company_id)
        .first()
    )

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    db_document = Document(
        company_id=company_id,
        document_type=document.document_type,
        title=document.title,
        filename=document.filename,
        mime_type=document.mime_type,
        file_size=document.file_size,
        file_data=document.file_data,
        content_text=document.content_text,
        notes=document.notes,
    )

    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    return db_document


@router.get("/{company_id}/documents", response_model=list[DocumentRead])
def list_company_documents(company_id: int, db: Session = Depends(get_db)):
    company = (
        db.query(Company)
        .filter(Company.id == company_id)
        .first()
    )

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    return (
        db.query(Document)
        .filter(Document.company_id == company_id)
        .order_by(Document.id)
        .all()
    )


@router.get("/{company_id}/documents/{document_id}", response_model=DocumentRead)
def get_company_document(
    company_id: int,
    document_id: int,
    db: Session = Depends(get_db),
):
    document = (
        db.query(Document)
        .filter(Document.company_id == company_id, Document.id == document_id)
        .first()
    )

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    return document
