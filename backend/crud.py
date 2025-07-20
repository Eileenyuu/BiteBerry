from sqlalchemy.orm import Session
from models import UserPreferences, DietaryRestriction
from schemas import UserPreferencesBase, UserPreferencesCreate, UserPreferencesUpdate
from typing import Optional
import logging

logger = logging.getLogger(__name__)

def create_user_preferences(db: Session, prefs: UserPreferencesCreate) -> UserPreferences:
    """
    Create new user preferences in the database.
    Returns the created preferences.
    """
    try:
        new_prefs = UserPreferences(**prefs.dict())
        db.add(new_prefs)
        db.commit()
        db.refresh(new_prefs)
        return new_prefs
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating user preferencees: {e}")
        raise

def get_user_preferences(db: Session, prefs_id: int) -> Optional[UserPreferences]:
    """
    Get the user preferences from the database.
    If no preferences exist, returns None.
    """
    try:
        return db.query(UserPreferences).filter_by(id=prefs_id).first()
    except Exception as e:
        logger.error(f'Error retrieving user preferences: {e}')
        return None

def update_user_preferences(db: Session, prefs_id: int, updates: UserPreferencesUpdate) -> Optional[UserPreferences]:
    """
    Update existing user preferences in the database.
    Returns the updated preferences or None if not found.
    """
    try:
        prefs = get_user_preferences(db, prefs_id)
        if not prefs:
            return None
        
        for field, value in updates.dict(exclude_unset=True).items():
            setattr(prefs, field, value)
        
        db.commit()
        db.refresh(prefs)
        return prefs
    except Exception as e:
        db.rollback()
        logger.error(f'Error updating user preferences: {e}')
        raise

def delete_user_preferences(db: Session, prefs_id: int) -> bool:
    """
    Delete user preferences from the database.
    Returns True if successful, False if not found.
    """
    try:
        prefs = get_user_preferences(db, prefs_id)
        if not prefs:
            return False
        
        db.delete(prefs)
        db.commit()
        return True
    except Exception as e:
        logger.error(f'Error deleting user preferences: {e}')
        raise
