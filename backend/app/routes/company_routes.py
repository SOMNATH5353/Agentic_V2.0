from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..dependencies import get_db
from ..models.company import Company

router = APIRouter(prefix="/company", tags=["Company"])

@router.post("/")
def create_company(name: str, description: str, db: Session = Depends(get_db)):
    company = Company(name=name, description=description)
    db.add(company)
    db.commit()
    db.refresh(company)
    return company
