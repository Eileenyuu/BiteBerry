from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Enum, ForeignKey, UniqueConstraint, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum as PyEnum

Base = declarative_base()

# ============================================
# Enums
# ============================================

class DietaryRestriction(PyEnum):
    NONE = "none"
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    GLUTEN_FREE = "gluten_free"
    DAIRY_FREE = "dairy_free"
    NUT_FREE = "nut_free"
    KETO = "keto"
    PALEO = "paleo"

class DifficultyLevel(PyEnum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class MealType(PyEnum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"

# ============================================
# Core Models - MVP
# ============================================

class UserPreferences(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    max_budget = Column(Float, default=50.0, nullable=False)
    max_cooking_time = Column(Integer, default=30, nullable=False)
    dietary_restrictions = Column(Enum(DietaryRestriction), default=DietaryRestriction.NONE, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<UserPreferences(id={self.id}, max_budget={self.max_budget}, max_cooking_time={self.max_cooking_time}, dietary_restrictions={self.dietary_restrictions})>"

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"

class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=False)
    
    # JSON stored as text - ingredients and instructions arrays
    ingredients = Column(Text, nullable=False)  # JSON array of ingredients
    instructions = Column(Text, nullable=False)  # JSON array of instructions
    
    # Cooking details
    cooking_time = Column(Integer, nullable=False, index=True)  # minutes - indexed for filtering
    prep_time = Column(Integer, default=10)  # minutes
    difficulty = Column(Enum(DifficultyLevel), default=DifficultyLevel.EASY)
    servings = Column(Integer, default=2, nullable=False)
    
    # Cost and nutrition
    budget = Column(Float, nullable=False, index=True)  # total cost, not per serving - indexed for filtering
    calories_per_serving = Column(Integer, default=400)
    
    # Categories
    cuisine = Column(String(50))  # Japanese, Italian, etc.
    dietary_restrictions = Column(Enum(DietaryRestriction), default=DietaryRestriction.NONE, index=True)  # indexed for filtering
    
    # Media and metadata
    image_url = Column(String(500))  # placeholder or real image URLs
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # For future features
    is_featured = Column(Integer, default=0)  # 0=no, 1=yes (boolean as int for SQLite)
    average_rating = Column(Float, default=0.0)  # for future rating system

    def __repr__(self):
        return f"<Recipe(id={self.id}, title={self.title}, budget=£{self.budget})>"

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Ensure one user can only like a recipe once
    __table_args__ = (
        UniqueConstraint('user_id', 'recipe_id', name='unique_user_recipe_like'),
    )

    def __repr__(self):
        return f"<Like(user_id={self.user_id}, recipe_id={self.recipe_id})>"

class ShoppingList(Base):
    __tablename__ = "shopping_lists"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<ShoppingList(id={self.id}, name={self.name})>"

class ShoppingListItem(Base):
    __tablename__ = "shopping_list_items"
    
    id = Column(Integer, primary_key=True, index=True)
    list_id = Column(Integer, ForeignKey("shopping_lists.id"), nullable=False)
    ingredient = Column(String(200), nullable=False)
    quantity = Column(String(50), default="1")
    is_checked = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"<ShoppingListItem(id={self.id}, ingredient={self.ingredient})>"

class MealPlan(Base):
    __tablename__ = "meal_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    meal_date = Column(DateTime, nullable=False)  # Date for the meal
    meal_type = Column(String(50), nullable=False)  # breakfast, lunch, dinner
    servings = Column(Integer, default=2, nullable=False)  # How many servings planned
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<MealPlan(id={self.id}, date={self.meal_date.date()}, meal_type={self.meal_type})>"

