from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Enum
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

# ============================================
# Core Models - MVP
# ============================================

class UserPreferences(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    max_budget = Column(Float, default=50.0, nullable=False)
    max_cooking_time = Column(Integer, default=30, nullable=False)
    dietary_restrictions = Column(Enum(DietaryRestriction), default=DietaryRestriction.NONE, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<UserPreferences(id={self.id}, max_budget={self.max_budget}, max_cooking_time={self.max_cooking_time}, dietary_restrictions={self.dietary_restrictions})>"

class Recipe(Base):
    __tablename__ = 'recipes'

    recipe_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(128), nullable=False)
    description = Column(Text)
    ingredients_list = Column(Text, nullable=False)

    # time info
    cooking_time = Column(Integer)

    # budget info
    budget_per_serving = Column(Float)
    servings = Column(Integer, default=1)

    # other attributes
    cuisine_type = Column(String(128))

    def __repr__(self):
        return f"<Recipe(recipe_id={self.recipe_id}, title={self.title})>"

