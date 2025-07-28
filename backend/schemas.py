from pydantic import BaseModel, Field
from models import DietaryRestriction
from typing import Optional, List
from datetime import datetime
from config import DefaultPreferences, ValidationLimits

# ============================================
# Pydantic Models - For API request
# ============================================

# Recipe
class RecipeResponse(BaseModel):
    recipe_id: int
    title: str
    description: str
    ingredients_list: List[str]
    cooking_time: int
    budget_per_serving: float
    servings: int
    cuisine_type: str
    image_url: Optional[str] = None

# User Preferences
class UserPreferencesBase(BaseModel):
    max_budget: float = Field(gt=ValidationLimits.MIN_BUDGET, le=ValidationLimits.MAX_BUDGET, default=DefaultPreferences.MAX_BUDGET)
    max_cooking_time: int = Field(gt=ValidationLimits.MIN_COOKING_TIME, le=ValidationLimits.MAX_COOKING_TIME, default=DefaultPreferences.MAX_COOKING_TIME)
    dietary_restrictions: DietaryRestriction = Field(default=DietaryRestriction.NONE)

class UserPreferencesCreate(UserPreferencesBase):
    pass

class UserPreferencesResponse(UserPreferencesBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserPreferencesUpdate(BaseModel):
    max_budget: Optional[float] = Field(gt=ValidationLimits.MIN_BUDGET, le=ValidationLimits.MAX_BUDGET, default=None)
    max_cooking_time: Optional[int] = Field(gt=ValidationLimits.MIN_COOKING_TIME, le=ValidationLimits.MAX_COOKING_TIME, default=None)
    dietary_restrictions: Optional[DietaryRestriction] = Field(default=None)

