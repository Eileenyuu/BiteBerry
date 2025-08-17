import hashlib
from sqlalchemy.orm import Session
from core.models import User, UserPreferences, DietaryRestriction
from core.config import DefaultPreferences
from core.schemas import UserCreate, UserLogin
from datetime import datetime

def hash_password(password: str) -> str:
    """Simple password hashing using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return hash_password(password) == hashed_password

def create_user(db: Session, user_data: UserCreate) -> User:
    """Create a new user with default preferences"""
    # Check if username or email already exists
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()
    
    if existing_user:
        raise ValueError("Username or email already exists")
    
    # Create new user
    hashed_password = hash_password(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password
    )
    
    db.add(new_user)
    db.flush()  # Get the user ID without committing
    
    # Check if preferences already exist for this user (shouldn't happen, but just in case)
    existing_prefs = db.query(UserPreferences).filter(UserPreferences.user_id == new_user.id).first()
    if not existing_prefs:
        # Create default preferences for the new user
        default_preferences = UserPreferences(
            user_id=new_user.id,
            max_budget=DefaultPreferences.MAX_BUDGET,
            max_cooking_time=DefaultPreferences.MAX_COOKING_TIME,
            dietary_restrictions=DietaryRestriction.NONE,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(default_preferences)
    
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, login_data: UserLogin) -> User:
    """Authenticate user login"""
    user = db.query(User).filter(User.username == login_data.username).first()
    
    if not user:
        raise ValueError("Invalid username or password")
    
    if not verify_password(login_data.password, user.password_hash):
        raise ValueError("Invalid username or password")
    
    return user