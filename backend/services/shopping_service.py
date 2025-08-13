import json
from collections import Counter
from sqlalchemy.orm import Session
from datetime import datetime
from core.models import ShoppingList, ShoppingListItem, Recipe
from core.schemas import ShoppingListCreate
from services.meal_planning_service import get_meal_plans_by_date_range

def consolidate_ingredients(ingredient_list):
    """Consolidate duplicate ingredients using exact string matching"""
    # Normalize and count ingredients
    normalized_ingredients = []
    for ingredient in ingredient_list:
        normalized = ingredient.strip()
        normalized_ingredients.append(normalized)
    
    # Count occurrences
    ingredient_counts = Counter(normalized_ingredients)
    
    # Return list of (ingredient, count) tuples
    consolidated = []
    for ingredient, count in ingredient_counts.items():
        consolidated.append((ingredient, count))
    
    return consolidated

def create_list_from_recipes(db: Session, user_id: int, list_data: ShoppingListCreate):
    """Create shopping list from selected recipes with ingredient consolidation"""
    # Create the shopping list
    shopping_list = ShoppingList(
        user_id=user_id,
        name=list_data.name
    )
    db.add(shopping_list)
    db.commit()
    db.refresh(shopping_list)
    
    # Collect all ingredients from recipes (accounting for duplicates)
    all_ingredients = []
    
    for recipe_id in list_data.recipe_ids:  # Process each recipe ID separately
        recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
        if recipe:
            ingredients = json.loads(recipe.ingredients)
            all_ingredients.extend(ingredients)
    
    # Consolidate ingredients
    consolidated_ingredients = consolidate_ingredients(all_ingredients)
    
    # Add consolidated ingredients to shopping list
    for ingredient, count in consolidated_ingredients:
        item = ShoppingListItem(
            list_id=shopping_list.id,
            ingredient=ingredient,
            quantity=str(count)
        )
        db.add(item)
    
    db.commit()
    
    # Return the complete shopping list with items
    return get_shopping_list(db, shopping_list.id)

def get_user_lists(db: Session, user_id: int):
    """Get all shopping lists for a user"""
    return db.query(ShoppingList).filter(ShoppingList.user_id == user_id).all()

def get_shopping_list(db: Session, list_id: int):
    """Get a shopping list with its items"""
    shopping_list = db.query(ShoppingList).filter(ShoppingList.id == list_id).first()
    if shopping_list:
        items = db.query(ShoppingListItem).filter(ShoppingListItem.list_id == list_id).all()
        shopping_list.items = items
    return shopping_list

def toggle_item_checked(db: Session, item_id: int):
    """Toggle the checked status of a shopping list item"""
    item = db.query(ShoppingListItem).filter(ShoppingListItem.id == item_id).first()
    if item:
        item.is_checked = not item.is_checked
        db.commit()
        return item
    return None

def delete_shopping_list(db: Session, list_id: int, user_id: int):
    """Delete a shopping list and its items"""
    shopping_list = db.query(ShoppingList).filter(
        ShoppingList.id == list_id,
        ShoppingList.user_id == user_id
    ).first()
    
    if shopping_list:
        # Delete items first
        db.query(ShoppingListItem).filter(ShoppingListItem.list_id == list_id).delete()
        # Delete the list
        db.delete(shopping_list)
        db.commit()
        return True
    return False

def create_list_from_meal_plans(db: Session, user_id: int, start_date: datetime, end_date: datetime, list_name: str):
    """Create shopping list from meal plans in date range with consolidation"""
    # Get meal plans for date range
    meal_plans = get_meal_plans_by_date_range(db, user_id, start_date, end_date)
    
    # Extract recipe IDs (keep duplicates for proper ingredient counting)
    recipe_ids = [plan.recipe_id for plan in meal_plans]
    
    if not recipe_ids:
        return None
    
    # Use the consolidation logic by calling create_list_from_recipes
    list_data = ShoppingListCreate(name=list_name, recipe_ids=recipe_ids)
    return create_list_from_recipes(db, user_id, list_data)