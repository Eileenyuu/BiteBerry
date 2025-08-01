"""
Recommendation service for recipe suggestions
"""
from sqlalchemy.orm import Session
from core.models import Recipe, DietaryRestriction, Like
import json
import logging

logger = logging.getLogger(__name__)


def get_recipe_recommendations(
    db: Session,
    user_id: int, 
    final_budget: float,
    final_cooking_time: int,
    final_dietary_restrictions: DietaryRestriction
) -> list:
    """
    Get recipe recommendations based on user preferences
    
    Args:
        db: Database session
        user_id: User ID for like information
        final_budget: Maximum budget constraint
        final_cooking_time: Maximum cooking time constraint
        final_dietary_restrictions: Dietary restriction preference
        
    Returns:
        List of recommended recipe dictionaries
    """
    recommended_recipes = []
    recipes = db.query(Recipe).all()
    
    if recipes:  # Check if recipes exist
        for recipe in recipes:
            # Apply budget, time, and dietary restriction filters
            if (recipe.budget <= final_budget and 
                recipe.cooking_time <= final_cooking_time and
                (final_dietary_restrictions == DietaryRestriction.NONE or 
                 recipe.dietary_restrictions == final_dietary_restrictions)):
                
                # Get like information for this recipe
                like_count = db.query(Like).filter(Like.recipe_id == recipe.id).count()
                user_has_liked = db.query(Like).filter(
                    Like.user_id == user_id, 
                    Like.recipe_id == recipe.id
                ).first() is not None
                
                # Parse JSON only once and handle errors gracefully
                try:
                    ingredients = json.loads(recipe.ingredients) if recipe.ingredients else []
                except (json.JSONDecodeError, TypeError):
                    ingredients = []
                    logger.warning(f"Invalid ingredients JSON for recipe {recipe.id}")
                
                try:
                    instructions = json.loads(recipe.instructions) if recipe.instructions else []
                except (json.JSONDecodeError, TypeError):
                    instructions = []
                    logger.warning(f"Invalid instructions JSON for recipe {recipe.id}")
                
                # Convert to dict format for response (maintaining compatibility)
                recipe_data = {
                    'recipe_id': recipe.id,  # Keep frontend compatibility
                    'title': recipe.title,
                    'budget': recipe.budget,
                    'cooking_time': recipe.cooking_time,
                    'description': recipe.description,
                    'cuisine': recipe.cuisine,
                    'dietary': recipe.dietary_restrictions.value,
                    'servings': recipe.servings,
                    'ingredients': ingredients,
                    'instructions': instructions,
                    'like_count': like_count,
                    'user_has_liked': user_has_liked
                }
                recommended_recipes.append(recipe_data)
    
    return recommended_recipes