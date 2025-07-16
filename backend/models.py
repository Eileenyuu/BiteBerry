from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

Base = declarative_base()

# ============================================
# Core Models - MVP
# ============================================

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

# ============================================
# Pydantic Models - For API request
# ============================================
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

