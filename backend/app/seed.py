from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Organization, Vacancy

def run_seed() -> None:
    db: Session = SessionLocal()
    try:
        has_any = db.query(Organization).first()
        if has_any:
            return  # уже сидировано

        org = Organization(name="Test Org", description="Demo organization")
        db.add(org)
        db.flush()  # чтобы появился org.id

        vac = Vacancy(
            org_id=org.id,
            title="Junior Developer",
            description="Great opportunity",
            employment_type="full-time",
            location="Remote",
            is_active=True,
        )
        db.add(vac)
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    run_seed()
