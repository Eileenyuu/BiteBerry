"""
Recipe likes API routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from core.database import get_db
from core.models import Recipe, User, Like
from core.schemas import LikeResponse, RecipeLikeCount

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/recipes", tags=["likes"])


@router.post('/{recipe_id}/like/{user_id}', response_model=LikeResponse)
async def like_recipe(recipe_id: int, user_id: int, db: Session = Depends(get_db)):
    """Like a recipe (user can only like once)"""
    try:
        logger.info(f"User {user_id} attempting to like recipe {recipe_id}")
        
        # Check if recipe exists
        recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        
        # Check if user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if user already liked this recipe
        existing_like = db.query(Like).filter(
            Like.user_id == user_id, 
            Like.recipe_id == recipe_id
        ).first()
        
        if existing_like:
            # Already liked - just return the existing like
            logger.info(f"User {user_id} already liked recipe {recipe_id}")
            return existing_like
        
        # Create new like
        new_like = Like(
            user_id=user_id,
            recipe_id=recipe_id,
            created_at=datetime.utcnow()
        )
        
        db.add(new_like)
        db.commit()
        db.refresh(new_like)
        
        logger.info(f"User {user_id} successfully liked recipe {recipe_id}")
        return new_like
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error liking recipe: {e}")
        raise HTTPException(status_code=500, detail="Failed to like recipe")


@router.get('/{recipe_id}/likes/{user_id}', response_model=RecipeLikeCount)
async def get_recipe_like_info(recipe_id: int, user_id: int, db: Session = Depends(get_db)):
    """Get like count for a recipe and whether current user has liked it"""
    try:
        # Check if recipe exists
        recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        
        # Count total likes for this recipe
        like_count = db.query(Like).filter(Like.recipe_id == recipe_id).count()
        
        # Check if current user has liked this recipe
        user_has_liked = db.query(Like).filter(
            Like.user_id == user_id, 
            Like.recipe_id == recipe_id
        ).first() is not None
        
        return RecipeLikeCount(
            recipe_id=recipe_id,
            like_count=like_count,
            user_has_liked=user_has_liked
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting like info: {e}")
        raise HTTPException(status_code=500, detail="Failed to get like information")


@router.delete('/{recipe_id}/unlike/{user_id}')
async def unlike_recipe(recipe_id: int, user_id: int, db: Session = Depends(get_db)):
    """Unlike a recipe (remove like)"""
    try:
        logger.info(f"User {user_id} attempting to unlike recipe {recipe_id}")
        
        # Check if recipe exists
        recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        
        # Find the existing like
        existing_like = db.query(Like).filter(
            Like.user_id == user_id, 
            Like.recipe_id == recipe_id
        ).first()
        
        if not existing_like:
            # User hasn't liked this recipe
            raise HTTPException(status_code=404, detail="Like not found")
        
        # Delete the like
        db.delete(existing_like)
        db.commit()
        
        logger.info(f"User {user_id} successfully unliked recipe {recipe_id}")
        return {"message": "Recipe unliked successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error unliking recipe: {e}")
        raise HTTPException(status_code=500, detail="Failed to unlike recipe")