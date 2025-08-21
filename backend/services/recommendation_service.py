"""
Recommendation service for recipe suggestions
"""
from sqlalchemy.orm import Session
from core.models import Recipe, DietaryRestriction, Like
try:
    from services.ai_recommendation_service import ai_service
    AI_AVAILABLE = True
except ImportError as e:
    logger.warning(f"AI service not available: {e}")
    ai_service = None
    AI_AVAILABLE = False
from services.recipe_query_service import get_filtered_recipes_with_likes, get_recipe_count_by_filters
from services.recipe_serializer import serialize_recipe_list, serialize_recipe_data
import logging

logger = logging.getLogger(__name__)


def get_recipe_recommendations(
    db: Session,
    user_id: int, 
    final_budget: float,
    final_cooking_time: int,
    final_dietary_restrictions: DietaryRestriction,
    include_ai: bool = True,
    limit: int = 50,
    offset: int = 0
) -> dict:
    """
    Get recipe recommendations based on user preferences
    
    Args:
        db: Database session
        user_id: User ID for like information
        final_budget: Maximum budget constraint
        final_cooking_time: Maximum cooking time constraint
        final_dietary_restrictions: Dietary restriction preference
        include_ai: Whether to include AI-powered recommendations
        limit: Maximum number of recipes to return
        offset: Number of recipes to skip (for pagination)
        
    Returns:
        Dictionary with recipes list and pagination info
    """
    # Get filtered recipes with optimized query
    recipe_data_list = get_filtered_recipes_with_likes(
        db, user_id, final_budget, final_cooking_time, 
        final_dietary_restrictions, limit, offset
    )
    
    # Convert to standardized format (Convert to dictionary)
    recommended_recipes = serialize_recipe_list(recipe_data_list)
    
    # Add AI recommendations if enabled and available
    if include_ai and AI_AVAILABLE:
        recommended_recipes = _enhance_with_ai_recommendations(
            db, user_id, recommended_recipes, final_budget, 
            final_cooking_time, final_dietary_restrictions
        )
    
    # Sort recommendations
    recommended_recipes.sort(key=_get_sort_key)
    
    # Get total count for pagination
    total_count = get_recipe_count_by_filters(
        db, final_budget, final_cooking_time, final_dietary_restrictions
    )
    
    return {
        'recipes': recommended_recipes,
        'total_count': total_count,
        'limit': limit,
        'offset': offset,
        'has_more': offset + len(recommended_recipes) < total_count
    }


def _enhance_with_ai_recommendations(
    db: Session, user_id: int, existing_recipes: list,
    budget: float, cooking_time: int, dietary_restrictions: DietaryRestriction
) -> list:
    """Add AI recommendations to existing recipe list"""
    if not AI_AVAILABLE or ai_service is None:
        return existing_recipes
        
    try:
        ai_recommendations = ai_service.get_ai_recommendations(db, user_id, limit=3)
        ai_recipe_data = {ai_rec['recipe'].id: ai_rec for ai_rec in ai_recommendations}
        
        # Mark existing recipes as AI/popular if they match
        for recipe_data in existing_recipes:
            if recipe_data['id'] in ai_recipe_data:
                ai_rec = ai_recipe_data[recipe_data['id']]
                recipe_data['recommendation_type'] = ai_rec.get('recommendation_type', 'ai')
                recipe_data['ai_similarity_score'] = ai_rec['similarity_score']
        
        # Add new AI recommendations that aren't already included
        existing_recipe_ids = {r['id'] for r in existing_recipes}
        
        for ai_rec in ai_recommendations:
            recipe = ai_rec['recipe']
            
            if (_recipe_matches_filters(recipe, budget, cooking_time, dietary_restrictions) and
                recipe.id not in existing_recipe_ids):
                
                # Get like information
                like_count = db.query(Like).filter(Like.recipe_id == recipe.id).count()
                user_has_liked = db.query(Like).filter(
                    Like.user_id == user_id, Like.recipe_id == recipe.id
                ).first() is not None
                
                # Serialize with AI fields
                recipe_data = serialize_recipe_data(
                    recipe, like_count, user_has_liked,
                    ai_similarity_score=ai_rec['similarity_score'],
                    recommendation_type=ai_rec.get('recommendation_type', 'ai')
                )
                existing_recipes.append(recipe_data)
                
    except Exception as e:
        logger.warning(f"AI recommendations failed: {e}")
    
    return existing_recipes


def _recipe_matches_filters(recipe, budget: float, cooking_time: int, dietary_restrictions: DietaryRestriction) -> bool:
    """Check if recipe matches filtering criteria"""
    return (recipe.budget <= budget and 
            recipe.cooking_time <= cooking_time and
            (dietary_restrictions == DietaryRestriction.NONE or 
             recipe.dietary_restrictions == dietary_restrictions))


def _get_sort_key(recipe: dict) -> tuple:
    """Sort key for recommendations (AI/popular first, then by scores)"""
    recommendation_type = recipe.get('recommendation_type')
    is_ai_or_popular = 1 if recommendation_type in ['ai', 'popular'] else 0
    ai_score = recipe.get('ai_similarity_score', 0)
    like_count = recipe.get('like_count', 0)
    return (-is_ai_or_popular, -ai_score, -like_count)