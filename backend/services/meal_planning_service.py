from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from core.models import MealPlan, Recipe, MealType
from core.schemas import MealPlanCreate

def create_meal_plan(db: Session, user_id: int, meal_plan_data: MealPlanCreate):
    """Create a new meal plan entry"""
    meal_plan = MealPlan(
        user_id=user_id,
        recipe_id=meal_plan_data.recipe_id,
        meal_date=meal_plan_data.meal_date,
        meal_type=meal_plan_data.meal_type,
        servings=meal_plan_data.servings
    )
    
    db.add(meal_plan)
    db.commit()
    db.refresh(meal_plan)
    return meal_plan

def get_user_meal_plans(db: Session, user_id: int, start_date: datetime = None, end_date: datetime = None):
    """Get all meal plans for a user within a date range"""
    query = db.query(MealPlan).filter(MealPlan.user_id == user_id)
    
    if start_date:
        # Use date comparison to avoid timezone issues
        query = query.filter(func.date(MealPlan.meal_date) >= start_date.date())
    if end_date:
        # Use date comparison and include the end date by using the full day
        query = query.filter(func.date(MealPlan.meal_date) <= end_date.date())
    
    return query.order_by(MealPlan.meal_date, MealPlan.meal_type).all()

def get_weekly_meal_plan(db: Session, user_id: int, start_date: datetime):
    """Get meal plan for a specific week"""
    end_date = start_date + timedelta(days=6)  # 7 days total
    return get_user_meal_plans(db, user_id, start_date, end_date)

def update_meal_plan(db: Session, meal_plan_id: int, user_id: int, meal_plan_data: MealPlanCreate):
    """Update an existing meal plan"""
    meal_plan = db.query(MealPlan).filter(
        MealPlan.id == meal_plan_id,
        MealPlan.user_id == user_id
    ).first()
    
    if not meal_plan:
        return None
    
    meal_plan.recipe_id = meal_plan_data.recipe_id
    meal_plan.meal_date = meal_plan_data.meal_date
    meal_plan.meal_type = meal_plan_data.meal_type
    meal_plan.servings = meal_plan_data.servings
    
    db.commit()
    db.refresh(meal_plan)
    return meal_plan

def delete_meal_plan(db: Session, meal_plan_id: int, user_id: int):
    """Delete a meal plan"""
    meal_plan = db.query(MealPlan).filter(
        MealPlan.id == meal_plan_id,
        MealPlan.user_id == user_id
    ).first()
    
    if not meal_plan:
        return False
    
    db.delete(meal_plan)
    db.commit()
    return True

def get_meal_plans_by_date_range(db: Session, user_id: int, start_date: datetime, end_date: datetime):
    """Get meal plans for shopping list generation"""
    return db.query(MealPlan).filter(
        and_(
            MealPlan.user_id == user_id,
            func.date(MealPlan.meal_date) >= start_date.date(),
            func.date(MealPlan.meal_date) <= end_date.date()
        )
    ).all()

def check_meal_conflict(db: Session, user_id: int, meal_date: datetime, meal_type: str):
    """Check if there's already a meal planned for this slot"""
    # Convert to date for comparison to avoid timezone issues
    target_date = meal_date.date()
    
    existing_plan = db.query(MealPlan).filter(
        and_(
            MealPlan.user_id == user_id,
            func.date(MealPlan.meal_date) == target_date,
            MealPlan.meal_type == meal_type
        )
    ).first()
    
    return existing_plan is not None