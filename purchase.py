from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.purchase import Purchase
from app.models.sweet import Sweet
from app.models.user import User
from app.schemas.purchase import PurchaseCreate, PurchaseResponse
from app.core.security import get_current_user

router = APIRouter()


@router.post("/", response_model=PurchaseResponse, status_code=201)
def purchase_sweet(
    data: PurchaseCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    sweet = db.query(Sweet).filter(Sweet.id == data.sweet_id).first()

    if not sweet:
        raise HTTPException(404, "Sweet not found")

    if sweet.quantity < data.quantity:
        raise HTTPException(
            status_code=400,
            detail="Insufficient stock"
        )

    # 1️⃣ Reduce inventory
    sweet.quantity -= data.quantity

    # 2️⃣ Record purchase
    purchase = Purchase(
        user_id=user.id,
        sweet_id=sweet.id,
        quantity=data.quantity
    )

    db.add(purchase)
    db.commit()
    db.refresh(purchase)

    return purchase
