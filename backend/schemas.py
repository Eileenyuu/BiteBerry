from pydantic import BaseModel, Field, EmailStr
from models import DietaryRestriction, DifficultyLevel
from typing import Optional, List
from datetime import datetime
from config import DefaultPreferences, ValidationLimits
import json

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

# User Authentication
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str = EmailStr
    password: str = Field(min_length=6, max_length=50)

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

# Recipe schemas
class RecipeResponse(BaseModel):
    id: int
    title: str
    description: str
    ingredients: List[str]
    instructions: List[str]
    cooking_time: int
    prep_time: int
    difficulty: DifficultyLevel
    servings: int
    budget: float
    calories_per_serving: int
    cuisine: Optional[str] = None
    dietary_restrictions: DietaryRestriction
    image_url: Optional[str] = None
    is_featured: bool
    average_rating: float
    created_at: datetime

    @classmethod
    def from_orm(cls, recipe):
        """Convert Recipe model to RecipeResponse, parsing JSON fields"""
        return cls(
            id=recipe.id,
            title=recipe.title,
            description=recipe.description,
            ingredients=json.loads(recipe.ingredients) if recipe.ingredients else [],
            instructions=json.loads(recipe.instructions) if recipe.instructions else [],
            cooking_time=recipe.cooking_time,
            prep_time=recipe.prep_time,
            difficulty=recipe.difficulty,
            servings=recipe.servings,
            budget=recipe.budget,
            calories_per_serving=recipe.calories_per_serving,
            cuisine=recipe.cuisine,
            dietary_restrictions=recipe.dietary_restrictions,
            image_url=recipe.image_url,
            is_featured=bool(recipe.is_featured),
            average_rating=recipe.average_rating,
            created_at=recipe.created_at
        )

    class Config:
        from_attributes = True

# Like schemas
class LikeCreate(BaseModel):
    recipe_id: int

class LikeResponse(BaseModel):
    id: int
    user_id: int
    recipe_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class RecipeLikeCount(BaseModel):
    recipe_id: int
    like_count: int
    user_has_liked: bool