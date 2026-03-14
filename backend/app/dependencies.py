from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional
from app.database.session import get_db
from app.models.user import User
from app.services.auth_service import AuthService

async def get_current_user_id(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing auth header")

    try:
        token = authorization.split(" ")[1]
    except IndexError:
        raise HTTPException(status_code=401, detail="Invalid auth format")

    user_id = AuthService.verify_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid user")

    return str(user_id)

async def get_current_user(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
