from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.schemas.auth import UserCreate, UserLogin, TokenResponse, UserResponse
from app.services.auth_service import AuthService
from app.database.session import get_db
from app.models.user import User
from app.config import settings
from app.dependencies import get_current_user

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user_data.email.lower()).first():
        raise HTTPException(status_code=400, detail="Email exists")

    user = AuthService.create_user(db, user_data.email, user_data.password, user_data.full_name)
    return user

@router.post("/login", response_model=TokenResponse)
async def login(creds: UserLogin, db: Session = Depends(get_db)):
    user = AuthService.authenticate_user(db, creds.email, creds.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = AuthService.create_access_token(str(user.id))
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": settings.JWT_EXPIRATION_HOURS * 3600,
        "user": {
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "is_active": user.is_active
        }
    }

@router.get("/me", response_model=UserResponse)
async def get_me(user: User = Depends(get_current_user)):
    return user
