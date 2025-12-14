from fastapi import APIRouter, Depends
from app.core.security import get_current_user

router = APIRouter()

@router.get("/protected")
def protected_route(current_user = Depends(get_current_user)):
    return {
        "message": "You are authorized",
        "user_id": current_user.id,
        "email": current_user.email,
    }
