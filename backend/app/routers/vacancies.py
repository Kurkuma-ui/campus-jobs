from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..db import get_db
from ..models import Vacancy
from ..schemas import VacancyOut, VacanciesPage

router = APIRouter(prefix="/vacancies", tags=["vacancies"])

@router.get("", response_model=VacanciesPage)
def list_vacancies(
    db: Session = Depends(get_db),
    q: str | None = Query(None, description="search in title/description"),
    location: str | None = None,
    employment_type: str | None = None,
    is_active: bool | None = True,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    query = db.query(Vacancy)
    if q:
        like = f"%{q}%"
        query = query.filter(or_(Vacancy.title.ilike(like), Vacancy.description.ilike(like)))
    if location:
        query = query.filter(Vacancy.location.ilike(f"%{location}%"))
    if employment_type:
        query = query.filter(Vacancy.employment_type == employment_type)
    if is_active is not None:
        query = query.filter(Vacancy.is_active == is_active)

    total = query.count()
    items = query.order_by(Vacancy.created_at.desc()).offset(offset).limit(limit).all()
    return VacanciesPage(items=items, total=total, limit=limit, offset=offset)

@router.get("/{vacancy_id}", response_model=VacancyOut)
def get_vacancy(vacancy_id: int, db: Session = Depends(get_db)):
    vac = db.get(Vacancy, vacancy_id)
    if not vac:
        from fastapi import HTTPException, status
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Vacancy not found")
    return vac
