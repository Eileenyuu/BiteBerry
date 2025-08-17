"""
Recipe data serialization service
"""
import json
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


def serialize_recipe_data(recipe, like_count: int, user_has_liked: bool, **extra_fields) -> Dict[str, Any]:
    """
    Convert recipe model to dictionary format with like information
    
    Args:
        recipe: Recipe model instance
        like_count: Number of likes for this recipe
        user_has_liked: Whether current user has liked this recipe
        **extra_fields: Additional fields to include (e.g., ai_similarity_score)
        
    Returns:
        Dictionary representation of recipe
    """
    # Parse JSON fields safely
    ingredients = _parse_json_field(recipe.ingredients, recipe.id, "ingredients")
    instructions = _parse_json_field(recipe.instructions, recipe.id, "instructions")
    
    recipe_data = {
        'id': recipe.id,
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
    
    # Add any extra fields
    recipe_data.update(extra_fields)
    
    return recipe_data


def _parse_json_field(json_str: str, recipe_id: int, field_name: str) -> List:
    """
    Safely parse JSON field with error handling
    """
    try:
        return json.loads(json_str) if json_str else []
    except (json.JSONDecodeError, TypeError):
        logger.warning(f"Invalid {field_name} JSON for recipe {recipe_id}")
        return []


def serialize_recipe_list(recipe_data_list: List[tuple], **common_extra_fields) -> List[Dict[str, Any]]:
    """
    Serialize a list of (recipe, like_count, user_has_liked) tuples
    """
    return [
        serialize_recipe_data(recipe, like_count, user_has_liked, **common_extra_fields)
        for recipe, like_count, user_has_liked in recipe_data_list
    ]