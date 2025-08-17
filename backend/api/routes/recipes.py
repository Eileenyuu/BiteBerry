"""
Recipe-related API routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging

from core.database import get_db
from core.models import Recipe, DietaryRestriction, UserPreferences, Like
from core.schemas import RecipeResponse
from core.config import DefaultPreferences
from services.recommendation_service import get_recipe_recommendations

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/recipes", tags=["recipes"])


@router.get("/")
async def get_all_recipes(user_id: int = None, db: Session = Depends(get_db)):
    """Get all recipes with like information"""
    try:
        recipes = db.query(Recipe).all()
        result = []
        
        for recipe in recipes:
            # Parse JSON fields
            import json
            ingredients = json.loads(recipe.ingredients) if recipe.ingredients else []
            instructions = json.loads(recipe.instructions) if recipe.instructions else []
            
            # Get like information
            like_count = db.query(Like).filter(Like.recipe_id == recipe.id).count()
            user_has_liked = False
            if user_id:
                user_has_liked = db.query(Like).filter(
                    Like.user_id == user_id, 
                    Like.recipe_id == recipe.id
                ).first() is not None
            
            recipe_data = {
                'id': recipe.id,
                'title': recipe.title,
                'description': recipe.description,
                'ingredients': ingredients,
                'instructions': instructions,
                'cooking_time': recipe.cooking_time,
                'prep_time': recipe.prep_time,
                'difficulty': recipe.difficulty.value,
                'servings': recipe.servings,
                'budget': recipe.budget,
                'calories_per_serving': recipe.calories_per_serving,
                'cuisine': recipe.cuisine,
                'dietary_restrictions': recipe.dietary_restrictions.value,
                'image_url': recipe.image_url,
                'is_featured': bool(recipe.is_featured),
                'average_rating': recipe.average_rating,
                'created_at': recipe.created_at,
                'like_count': like_count,
                'user_has_liked': user_has_liked
            }
            result.append(recipe_data)
        
        return result
    except Exception as e:
        logger.error(f"Error retrieving recipes: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve recipes")


@router.get("/{recipe_id}", response_model=RecipeResponse)
async def get_recipe_detail(recipe_id: int, db: Session = Depends(get_db)):
    """Get detailed information for a specific recipe"""
    try:
        recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()

        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")

        return RecipeResponse.from_orm(recipe)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving recipe {recipe_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve recipe")


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


@router.get("/recommend/{user_id}")
async def recommend_recipe(
    user_id: int, 
    max_budget: float = None, 
    max_cooking_time: int = None, 
    dietary_restrictions: str = None,
    enable_ai: bool = True,
    db: Session = Depends(get_db)
):
    """
    Get recipe recommendations based on budget and cooking time constraints.
    
    Parameters will be resolved in this priority order:
    1. Query parameters (if provided)
    2. User's saved preferences (from database)
    3. System default values
    
    Args:
        user_id: User ID to get recommendations for
        max_budget: Optional budget override
        max_cooking_time: Optional cooking time override  
        dietary_restrictions: Optional dietary restriction override
        enable_ai: Whether to include AI-powered recommendations (default: True)
    """
    try:
        # Get user preferences from database
        user_preferences = get_or_create_preferences(db, user_id)
        
        # Validate query parameters first
        if max_budget is not None and max_budget <= 0:
            raise HTTPException(status_code=400, detail="Budget must be a positive value")
        if max_cooking_time is not None and max_cooking_time <= 0:
            raise HTTPException(status_code=400, detail="Cooking time must be a positive value")
        
        # Use provided parameters or fall back to stored preferences
        final_budget = max_budget if max_budget is not None else user_preferences.max_budget
        final_cooking_time = max_cooking_time if max_cooking_time is not None else user_preferences.max_cooking_time
        
        # Handle dietary restrictions parameter
        if dietary_restrictions is not None:
            try:
                final_dietary_restrictions = DietaryRestriction(dietary_restrictions)
            except ValueError:
                final_dietary_restrictions = user_preferences.dietary_restrictions
        else:
            final_dietary_restrictions = user_preferences.dietary_restrictions
        
        # Get recommendations using service
        recommendation_result = get_recipe_recommendations(
            db=db,
            user_id=user_id,
            final_budget=final_budget,
            final_cooking_time=final_cooking_time,
            final_dietary_restrictions=final_dietary_restrictions,
            include_ai=enable_ai
        )
        
        # Extract recipes list from new paginated response
        recommended_recipes = recommendation_result['recipes']
        
        # Separate AI and regular recommendations for better frontend display
        ai_recommendations = [r for r in recommended_recipes if r.get('recommendation_type') == 'ai']
        regular_recommendations = [r for r in recommended_recipes if r.get('recommendation_type') != 'ai']
        
        # Prepare response with proper structure
        response = {
            'filters': {
                'max_budget': final_budget,
                'max_cooking_time': final_cooking_time,
                'dietary_restrictions': final_dietary_restrictions.value
            },
            'recommendations': recommended_recipes,
            'total_count': recommendation_result['total_count'],
            'ai_count': len(ai_recommendations),
            'regular_count': len(regular_recommendations),
            'has_ai_recommendations': len(ai_recommendations) > 0,
            'pagination': {
                'limit': recommendation_result['limit'],
                'offset': recommendation_result['offset'],
                'has_more': recommendation_result['has_more']
            }
        }
        
        # Add suggestion message if no results found
        if not recommended_recipes:
            response['message'] = "No recipes found matching your criteria. Try increasing your budget or cooking time."
        
        logger.info(f"Returning {len(recommended_recipes)} recommendations for budget=${final_budget}, time={final_cooking_time}min")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in recommend_recipe: {e}")
        raise HTTPException(status_code=500, detail="Failed to get recommendations")