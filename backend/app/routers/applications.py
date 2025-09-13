from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Application, Vacancy
from ..schemas import ApplicationCreate, ApplicationOut
from ..auth import require_student, User  # type: ignore

router = APIRouter(prefix="/applications", tags=["applications"])

@router.post("", response_model=ApplicationOut, status_code=201)
def create_application(
    payload: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student),
):
    # проверим, что вакансия существует и активна
    vac = db.get(Vacancy, payload.vacancy_id)
    if not vac or not vac.is_active:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Vacancy is not available")

    app = Application(
        vacancy_id=payload.vacancy_id,
        student_id=current_user.id,
        cover_letter=payload.cover_letter,
        status="submitted",
    )
    db.add(app)
    db.commit()
    db.refresh(app)
    return app

@router.get("/me", response_model=list[ApplicationOut])
def my_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student),
):
    items = db.query(Application).filter(Application.student_id == current_user.id).order_by(Application.created_at.desc()).all()
    return items
