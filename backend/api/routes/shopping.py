from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from core.database import get_db
from core.schemas import ShoppingList, ShoppingListCreate
from services.shopping_service import (
    create_list_from_recipes,
    get_user_lists,
    get_shopping_list,
    toggle_item_checked,
    delete_shopping_list,
    create_list_from_meal_plans
)

router = APIRouter(prefix="/shopping", tags=["shopping"])

@router.post("/lists", response_model=ShoppingList)
async def create_shopping_list(
    list_data: ShoppingListCreate,
    user_id: int,  # In a real app, this would come from authentication
    db: Session = Depends(get_db)
):
    """Create a shopping list from selected recipes"""
    if not list_data.recipe_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one recipe must be selected"
        )
    
    return create_list_from_recipes(db, user_id, list_data)

@router.get("/lists", response_model=List[ShoppingList])
async def get_shopping_lists(
    user_id: int,  # In a real app, this would come from authentication
    db: Session = Depends(get_db)
):
    """Get all shopping lists for a user"""
    lists = get_user_lists(db, user_id)
    
    # Add items to each list
    for shopping_list in lists:
        complete_list = get_shopping_list(db, shopping_list.id)
        shopping_list.items = complete_list.items if complete_list else []
    
    return lists

@router.get("/lists/{list_id}", response_model=ShoppingList)
async def get_shopping_list_detail(
    list_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific shopping list with items"""
    shopping_list = get_shopping_list(db, list_id)
    if not shopping_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shopping list not found"
        )
    return shopping_list

@router.patch("/items/{item_id}/toggle")
async def toggle_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Toggle the checked status of a shopping list item"""
    item = toggle_item_checked(db, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shopping list item not found"
        )
    return {"success": True, "is_checked": item.is_checked}

@router.delete("/lists/{list_id}")
async def delete_list(
    list_id: int,
    user_id: int,  # In a real app, this would come from authentication
    db: Session = Depends(get_db)
):
    """Delete a shopping list"""
    success = delete_shopping_list(db, list_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shopping list not found"
        )
    return {"success": True}

@router.post("/from-meal-plans", response_model=ShoppingList)
async def create_from_meal_plans(
    user_id: int,
    start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(..., description="End date in YYYY-MM-DD format"),
    list_name: str = Query("Weekly Shopping List", description="Name for the shopping list"),
    db: Session = Depends(get_db)
):
    """Create shopping list from meal plans in date range"""
    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        
        shopping_list = create_list_from_meal_plans(db, user_id, start_dt, end_dt, list_name)
        
        if not shopping_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No meal plans found for the specified date range"
            )
        
        return shopping_list
        
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Use YYYY-MM-DD"
        )