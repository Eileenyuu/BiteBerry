from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional

from core.database import get_db
from core.schemas import MealPlan, MealPlanCreate, WeeklyMealPlan
from services.meal_planning_service import (
    create_meal_plan,
    get_user_meal_plans,
    get_weekly_meal_plan,
    update_meal_plan,
    delete_meal_plan,
    check_meal_conflict
)

router = APIRouter(prefix="/meal-planning", tags=["meal-planning"])

@router.post("/plans", response_model=MealPlan)
async def add_meal_plan(
    meal_plan_data: MealPlanCreate,
    user_id: int,  # In a real app, this would come from authentication
    db: Session = Depends(get_db)
):
    """Add a recipe to meal plan"""
    # Check for conflict (optional - can allow multiple meals per slot)
    has_conflict = check_meal_conflict(
        db, user_id, meal_plan_data.meal_date, meal_plan_data.meal_type
    )
    
    if has_conflict:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A meal is already planned for {meal_plan_data.meal_type} on {meal_plan_data.meal_date.date()}"
        )
    
    return create_meal_plan(db, user_id, meal_plan_data)

@router.get("/plans", response_model=List[MealPlan])
async def get_meal_plans(
    user_id: int,
    start_date: Optional[str] = Query(None, description="YYYY-MM-DD format"),
    end_date: Optional[str] = Query(None, description="YYYY-MM-DD format"),
    db: Session = Depends(get_db)
):
    """Get meal plans for a user within date range"""
    start_dt = None
    end_dt = None
    
    if start_date:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    if end_date:
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    
    return get_user_meal_plans(db, user_id, start_dt, end_dt)

@router.get("/weekly", response_model=WeeklyMealPlan)
async def get_weekly_plan(
    user_id: int,
    week_start: str = Query(..., description="Monday date in YYYY-MM-DD format"),
    db: Session = Depends(get_db)
):
    """Get meal plan for a specific week"""
    try:
        start_date = datetime.strptime(week_start, "%Y-%m-%d")
        end_date = start_date + timedelta(days=6)
        
        meal_plans = get_weekly_meal_plan(db, user_id, start_date)
        
        return WeeklyMealPlan(
            start_date=week_start,
            end_date=end_date.strftime("%Y-%m-%d"),
            meal_plans=meal_plans
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Use YYYY-MM-DD"
        )

@router.put("/plans/{meal_plan_id}", response_model=MealPlan)
async def update_meal_plan_endpoint(
    meal_plan_id: int,
    meal_plan_data: MealPlanCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Update a meal plan"""
    updated_plan = update_meal_plan(db, meal_plan_id, user_id, meal_plan_data)
    if not updated_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal plan not found"
        )
    return updated_plan

@router.delete("/plans/{meal_plan_id}")
async def delete_meal_plan_endpoint(
    meal_plan_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Delete a meal plan"""
    success = delete_meal_plan(db, meal_plan_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal plan not found"
        )
    return {"success": True}