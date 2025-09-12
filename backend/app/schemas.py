from pydantic import BaseModel, EmailStr, Field

class UserRegister(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=200)
    password: str = Field(min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    class Config:
        from_attributes = True


from typing import Optional, List

class VacancyOut(BaseModel):
    id: int
    org_id: int
    title: str
    description: str
    employment_type: Optional[str] = None
    location: Optional[str] = None
    is_active: bool
    class Config:
        from_attributes = True

class VacanciesPage(BaseModel):
    items: List[VacancyOut]
    total: int
    limit: int
    offset: int

class ApplicationCreate(BaseModel):
    vacancy_id: int
    cover_letter: Optional[str] = None

class ApplicationOut(BaseModel):
    id: int
    vacancy_id: int
    student_id: int
    status: str
    cover_letter: Optional[str] = None
    class Config:
        from_attributes = True
