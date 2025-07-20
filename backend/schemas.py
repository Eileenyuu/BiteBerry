from pydantic import BaseModel, Field
from models import DietaryRestriction
from typing import Optional, List
from datetime import datetime

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
    max_budget: float = Field(gt=0, le=100, default=50.0)
    max_cooking_time: int = Field(gt=0, le=180, default=30)
    dietary_restrictions: DietaryRestriction = Field(default=DietaryRestriction.NONE)

class UserPreferencesCreate(UserPreferencesBase):
    pass

class UserPreferencesResponse(UserPreferencesBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UserPreferencesUpdate(UserPreferencesBase):
    max_budget: Optional[float] = Field(gt=0, le=100, default=None)
    max_cooking_time: Optional[int] = Field(gt=0, le=180, default=None)
    dietary_restrictions: Optional[DietaryRestriction] = Field(default=None)

