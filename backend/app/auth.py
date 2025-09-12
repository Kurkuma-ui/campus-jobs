import os
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt
from passlib.context import CryptContext

from .db import get_db
from .models import User
from .schemas import UserRegister, UserLogin, Token

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
ALGORITHM = "HS256"
ACCESS_MIN = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pwd(p: str) -> str: return pwd_context.hash(p)
def verify_pwd(p: str, h: str) -> bool: return pwd_context.verify(p, h)

def make_token(data: dict, minutes: int = ACCESS_MIN) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(minutes=minutes)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register", response_model=Token, status_code=201)
def register(body: UserRegister, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == body.email).first():
        raise HTTPException(400, "Email already registered")
    user = User(
        email=body.email,
        full_name=body.full_name,
        role="student",
        password_hash=hash_pwd(body.password),
    )
    db.add(user); db.commit(); db.refresh(user)
    token = make_token({"sub": str(user.id), "email": user.email, "role": user.role})
    return Token(access_token=token)

@router.post("/login", response_model=Token)
def login(body: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == body.email).first()
    if not user or not verify_pwd(body.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
    token = make_token({"sub": str(user.id), "email": user.email, "role": user.role})
    return Token(access_token=token)
