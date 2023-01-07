from typing import List

from fastapi import APIRouter, Depends

from app.db.dependencies import get_db
from app.universities.crud.university import list_universities
from app.universities.schemas.reports import UniversityReport

router = APIRouter()


@router.get("/universities", response_model=List[UniversityReport])
async def universities_report(db=Depends(get_db)):
    universities_orm = list_universities(db, page_size=50)
    universities = [UniversityReport.from_orm(u) for u in universities_orm]
    return universities
