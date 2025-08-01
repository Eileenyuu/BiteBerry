"""
Authentication-related API routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging

from core.database import get_db
from core.schemas import UserCreate, UserLogin, UserResponse
from services import auth_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["authentication"])

@router.post('/register', response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        logger.info(f"Registration request received for user: {user_data.username}, email: {user_data.email}")
        new_user = auth_service.create_user(db, user_data)
        logger.info(f"User registered successfully: {new_user.username} (ID: {new_user.id})")
        return new_user
    except ValueError as e:
        logger.warning(f"Registration failed for {user_data.username}: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error during registration for {user_data.username}: {e}")
        raise HTTPException(status_code=500, detail="Registration failed")


@router.post('/login')
async def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """User login"""
    try:
        logger.info(f"Login attempt for user: {login_data.username}")
        user = auth_service.authenticate_user(db, login_data)
        logger.info(f"User logged in successfully: {user.username}")
        return {
            "message": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }
    except ValueError as e:
        logger.warning(f"Login failed: {e}")
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        logger.error(f"Error during login: {e}")
        raise HTTPException(status_code=500, detail="Login failed")