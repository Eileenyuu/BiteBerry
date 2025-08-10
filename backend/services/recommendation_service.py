"""
Recommendation service for recipe suggestions
"""
from sqlalchemy.orm import Session
from core.models import Recipe, DietaryRestriction, Like
from services.ai_recommendation_service import ai_service
import json
import logging

logger = logging.getLogger(__name__)


def get_recipe_recommendations(
    db: Session,
    user_id: int, 
    final_budget: float,
    final_cooking_time: int,
    final_dietary_restrictions: DietaryRestriction,
    include_ai: bool = True
) -> list:
    """
    Get recipe recommendations based on user preferences
    
    Args:
        db: Database session
        user_id: User ID for like information
        final_budget: Maximum budget constraint
        final_cooking_time: Maximum cooking time constraint
        final_dietary_restrictions: Dietary restriction preference
        include_ai: Whether to include AI-powered recommendations
        
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
                    'id': recipe.id,  # Use 'id' for consistency with recipes API
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
    
    # Add AI recommendations if enabled and user has liked recipes
    if include_ai:
        try:
            ai_recommendations = ai_service.get_ai_recommendations(db, user_id, limit=3)
            
            # Mark AI/popular recommendations in existing list instead of filtering duplicates
            ai_recipe_data = {ai_rec['recipe'].id: ai_rec for ai_rec in ai_recommendations}
            
            # First, mark existing recipes as AI/popular recommendations if they match
            for recipe_data in recommended_recipes:
                if recipe_data['id'] in ai_recipe_data:
                    ai_rec = ai_recipe_data[recipe_data['id']]
                    recipe_data['recommendation_type'] = ai_rec.get('recommendation_type', 'ai')
                    recipe_data['ai_similarity_score'] = ai_rec['similarity_score']
            
            # Then add any AI recommendations that aren't already in the list
            existing_recipe_ids = {r['id'] for r in recommended_recipes}
            
            for ai_rec in ai_recommendations:
                recipe = ai_rec['recipe']
                
                # Apply same constraints as regular recommendations
                if (recipe.budget <= final_budget and 
                    recipe.cooking_time <= final_cooking_time and
                    (final_dietary_restrictions == DietaryRestriction.NONE or 
                     recipe.dietary_restrictions == final_dietary_restrictions) and
                    recipe.id not in existing_recipe_ids):
                    
                    # Get like information for this recipe
                    like_count = db.query(Like).filter(Like.recipe_id == recipe.id).count()
                    user_has_liked = db.query(Like).filter(
                        Like.user_id == user_id, 
                        Like.recipe_id == recipe.id
                    ).first() is not None
                    
                    # Parse JSON safely
                    try:
                        ingredients = json.loads(recipe.ingredients) if recipe.ingredients else []
                    except (json.JSONDecodeError, TypeError):
                        ingredients = []
                    
                    try:
                        instructions = json.loads(recipe.instructions) if recipe.instructions else []
                    except (json.JSONDecodeError, TypeError):
                        instructions = []
                    
                    # Create recipe data with AI/popular type
                    recipe_data = {
                        'id': recipe.id,  # Use 'id' for consistency
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
                        'user_has_liked': user_has_liked,
                        'ai_similarity_score': ai_rec['similarity_score'],
                        'recommendation_type': ai_rec.get('recommendation_type', 'ai')
                    }
                    recommended_recipes.append(recipe_data)
                    
        except Exception as e:
            logger.warning(f"AI recommendations failed, continuing with basic recommendations: {e}")
    
    # Sort recommendations to put AI/popular suggestions first, then by like count
    def sort_key(recipe):
        recommendation_type = recipe.get('recommendation_type')
        is_ai_or_popular = 1 if recommendation_type in ['ai', 'popular'] else 0
        ai_score = recipe.get('ai_similarity_score', 0)
        like_count = recipe.get('like_count', 0)
        return (-is_ai_or_popular, -ai_score, -like_count)
    
    recommended_recipes.sort(key=sort_key)
    
    return recommended_recipes