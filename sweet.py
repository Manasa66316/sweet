from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.sweet import Sweet
from app.schemas.sweet import SweetCreate, SweetUpdate, SweetResponse
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()


def admin_only(user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(403, "Admin access required")
    return user


@router.post("/", response_model=SweetResponse, status_code=201)
def create_sweet(
    sweet: SweetCreate,
    db: Session = Depends(get_db),
    _: User = Depends(admin_only),
):
    if db.query(Sweet).filter(Sweet.name == sweet.name).first():
        raise HTTPException(400, "Sweet already exists")

    new_sweet = Sweet(**sweet.dict())
    db.add(new_sweet)
    db.commit()
    db.refresh(new_sweet)
    return new_sweet


@router.get("/", response_model=list[SweetResponse])
def list_sweets(db: Session = Depends(get_db)):
    return db.query(Sweet).all()


@router.put("/{sweet_id}", response_model=SweetResponse)
def update_sweet(
    sweet_id: int,
    sweet: SweetUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(admin_only),
):
    db_sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()
    if not db_sweet:
        raise HTTPException(404, "Sweet not found")

    for key, value in sweet.dict(exclude_unset=True).items():
        setattr(db_sweet, key, value)

    db.commit()
    db.refresh(db_sweet)
    return db_sweet


@router.delete("/{sweet_id}", status_code=204)
def delete_sweet(
    sweet_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(admin_only),
):
    sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()
    if not sweet:
        raise HTTPException(404, "Sweet not found")

    db.delete(sweet)
    db.commit()
