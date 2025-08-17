"""
Optimized recipe query service for scalable recommendations
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from core.models import Recipe, DietaryRestriction, Like
from typing import List, Tuple, Optional


def get_filtered_recipes_with_likes(
    db: Session,
    user_id: int,
    budget: float,
    cooking_time: int,
    dietary_restrictions: DietaryRestriction,
    limit: int = 50,
    offset: int = 0
) -> List[Tuple]:
    """
    Get filtered recipes with like counts in a single optimized query
    
    Args:
        db: Database session
        user_id: User ID for like information
        budget: Maximum budget constraint
        cooking_time: Maximum cooking time constraint
        dietary_restrictions: Dietary restriction preference
        limit: Maximum number of recipes to return
        offset: Number of recipes to skip (for pagination)
        
    Returns:
        List of tuples (Recipe, like_count, user_has_liked)
    """
    # Build base query with joins (SQLite-compatible)
    query = db.query(
        Recipe,
        func.count(Like.id).label('like_count'),
        func.max(func.coalesce(Like.user_id == user_id, 0)).label('user_has_liked')
    ).outerjoin(Like, Recipe.id == Like.recipe_id)
    
    # Apply filters
    query = query.filter(Recipe.budget <= budget)
    query = query.filter(Recipe.cooking_time <= cooking_time)
    
    if dietary_restrictions != DietaryRestriction.NONE:
        query = query.filter(Recipe.dietary_restrictions == dietary_restrictions)
    
    # Group by recipe to aggregate likes
    query = query.group_by(Recipe.id)
    
    # Add pagination
    query = query.limit(limit).offset(offset)
    
    return query.all()


def get_recipe_count_by_filters(
    db: Session,
    budget: float,
    cooking_time: int,
    dietary_restrictions: DietaryRestriction
) -> int:
    """
    Get total count of recipes matching filters (for pagination)
    """
    query = db.query(Recipe)
    query = query.filter(Recipe.budget <= budget)
    query = query.filter(Recipe.cooking_time <= cooking_time)
    
    if dietary_restrictions != DietaryRestriction.NONE:
        query = query.filter(Recipe.dietary_restrictions == dietary_restrictions)
    
    return query.count()