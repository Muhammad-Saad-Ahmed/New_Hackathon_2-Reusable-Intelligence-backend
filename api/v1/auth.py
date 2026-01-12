"""
Authentication API endpoints for the Todo Application backend.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Form, Request
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.task import UserCreate, User, MessageResponse
from models.database import User as UserModel
from core.security import get_password_hash, verify_password, create_access_token
from middleware.auth_middleware import JWTBearer
import uuid
from datetime import timedelta


router = APIRouter()


@router.post("/auth/register", response_model=User)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    """
    # Check if user already exists
    existing_user = db.query(UserModel).filter(UserModel.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists"
        )

    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = UserModel(
        email=user_data.email,
        name=user_data.name,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Return only the fields defined in the User schema (excluding hashed_password)
    return db_user


@router.post("/auth/login")
async def login_user(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    """
    Login a user and return a JWT token.
    """
    # Find the user by email
    user = db.query(UserModel).filter(UserModel.email == email).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(days=7)  # Token expires in 7 days
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/auth/me", response_model=User)
async def get_current_user(request: Request, db: Session = Depends(get_db), token_data: dict = Depends(JWTBearer())):
    """
    Get the current authenticated user's information.
    """
    try:
        user_id = uuid.UUID(token_data.get("sub"))
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )
    
    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Return only the fields defined in the User schema (excluding hashed_password)
    return user