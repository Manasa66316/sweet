from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.session import get_db
from app.models.user import User
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter()


class Register(BaseModel):
    email: str
    password: str


class Login(BaseModel):
    email: str
    password: str


@router.post("/register", status_code=201)
def register(data: Register, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(400, "Email already registered")

    user = User(
        email=data.email,
        hashed_password=hash_password(data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "email": user.email}


@router.post("/login")
def login(data: Login, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(400, "Invalid credentials")

    token = create_access_token({"sub": user.id})
    return {"access_token": token, "token_type": "bearer"}
