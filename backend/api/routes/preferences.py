"""
User preferences API routes
"""
from fastapi import APIRouter, Depends, HTTPException  
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from core.database import get_db
from core.models import UserPreferences, DietaryRestriction
from core.schemas import UserPreferencesUpdate, UserPreferencesResponse
from core.config import DefaultPreferences

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/preferences", tags=["preferences"])


def get_or_create_preferences(db: Session, user_id: int) -> UserPreferences:
    """Fetch User Preferences for specific user, if not exist, create default"""
    try:
        preferences = db.query(UserPreferences).filter(UserPreferences.user_id == user_id).first()
        if not preferences:
            logger.info(f"No preferences found for user {user_id}, creating default preferences")
            default_prefs = UserPreferences(
                user_id=user_id,
                max_budget=DefaultPreferences.MAX_BUDGET,
                max_cooking_time=DefaultPreferences.MAX_COOKING_TIME,
                dietary_restrictions=DietaryRestriction.NONE
            )
            db.add(default_prefs)
            db.commit()
            db.refresh(default_prefs)
            preferences = default_prefs
        return preferences
    except Exception as e:
        logger.error(f"Error getting or creating preferences: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get('/{user_id}', response_model=UserPreferencesResponse)
async def get_preferences(user_id: int, db: Session = Depends(get_db)):
    """Get user preferences for specific user"""
    try:
        logger.info(f"Fetching preferences for user {user_id}")
        preferences = get_or_create_preferences(db, user_id)
        return preferences
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving preferences: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve preferences")


@router.put('/{user_id}', response_model=UserPreferencesResponse)
async def update_preferences(user_id: int, preferences: UserPreferencesUpdate, db: Session = Depends(get_db)):
    """Update user preferences for specific user"""
    try:
        logger.info(f"Updating preferences for user {user_id}: {preferences.model_dump()}")
        
        # Fetch or Create current preferences
        current_pref = get_or_create_preferences(db, user_id)

        # Update preferences
        if preferences.max_budget is not None:
            current_pref.max_budget = preferences.max_budget
        if preferences.max_cooking_time is not None:
            current_pref.max_cooking_time = preferences.max_cooking_time
        if preferences.dietary_restrictions is not None:
            current_pref.dietary_restrictions = preferences.dietary_restrictions
            
        current_pref.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(current_pref)
        
        logger.info(f"Successfully updated preferences for user {user_id}")
        return current_pref
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating preferences: {e}")
        raise HTTPException(status_code=500, detail="Failed to update preferences")