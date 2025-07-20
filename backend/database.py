from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import logging
import os

from models import Base, UserPreferences

# Config logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Config SQLite database
SQLALCHEMY_DATABASE_URL = "sqlite:///./biteberry.db"

# Create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialise the database by creating all tables 
    and setting up default preferences if needed.
    """
    try:
        # 1. Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")

        # 2. Initialise default data
        # Check if user preferences exist, if not create default
        with SessionLocal() as db:
            preferences = db.query(UserPreferences).first()
            if not preferences:
                default_preferences = UserPreferences(
                    max_budget = 50.0,
                    max_cooking_time = 30,
                    dietary_restrictions = DietaryRestriction.NONE,
                )
                db.add(default_preferences)
                db.commit()
                logger.info("User preferences created")
            else:
                logger.info("User preferences already exist")
    except Exception as e:
        logger.error(f"Error initialising database: {e}")
        raise


def get_db() -> Generator[Session, None, None]: #Type hint: indicates the function is a generator yielding a session
    """Dependency for getting database session."""
    # Create db session
    db = SessionLocal()
    try:
        # Yields the session to FastAPI's dependency injection system
        yield db
    # Ensure the session is closed after the request is finished to aviod leaks.
    finally:
        db.close()

fake_recipes = [
    {
        'recipe_id': 1,
        'title': 'Chicken Teriyaki',
        'budget': 6.00,
        'cooking_time': 25,
        'description': 'Japanese-style glazed chicken with rice',
        'cuisine': 'Japanese',
        'dietary': None,
        'ingredients': ['chicken breast', 'soy sauce', 'mirin', 'sugar', 'rice']
    },
{
        'recipe_id': 2,
        'title': 'French Omelette',
        'budget': 3.00,
        'cooking_time': 10,
        'description': 'Classic French breakfast with herbs and cheese',
        'cuisine': 'French',
        'dietary': None,
        'ingredients': ['eggs', 'butter', 'herbs', 'cheese', 'salt']
    },
    {
        'recipe_id': 3,
        'title': 'BBQ Pulled Pork Burger',
        'budget': 7.80,
        'cooking_time': 25,
        'description': 'Tender pulled pork with tangy BBQ sauce on a soft bun',
        'cuisine': None,
        'dietary': None,
        'ingredients': ['pulled pork shoulder', 'grilled cheese', 'onion', 'salt']
    },
    {
        'recipe_id': 4,
        'title': 'Char Siu Pork',
        'budget': 7.50,
        'cooking_time': 40,
        'description': 'Cantonese BBQ pork with sweet and savory glaze',
        'cuisine': 'Chinese',
        'dietary': None,
        'ingredients': ['pork shoulder', 'honey', 'hoisin sauce', 'five-spice', 'salt']
    },
    {
        'recipe_id': 5,
        'title': 'Egg Fried Noodles',
        'budget': 3.50,
        'cooking_time': 15,
        'description': 'Quick Asian noodles with scrambled eggs and vegetables',
        'cuisine': None,
        'dietary': None,
        'ingredients': ['eggs', 'vegetables', 'noodles', 'salt']
    },
    {
        'recipe_id': 6,
        'title': 'Veggie Burrito Bowl',
        'budget': 4.50,
        'cooking_time': 18,
        'description': 'Mexican-inspired bowl with beans, rice, and fresh salsa',
        'cuisine': 'Mexican',
        'dietary': 'vegan',
        'ingredients': ['black beans', 'rice', 'salsa', 'onion', 'tomato', 'salt',
                        'pepper', 'cumin', 'garlic', 'chili powder',
                        'sugar', 'olive oil', 'vinegar', 'salt']
    },
    {
        'recipe_id': 7,
        'title': 'Simple Pasta Aglio e Olio',
        'budget': 2.50,
        'cooking_time': 15,
        'description': 'Italian pasta with garlic, olive oil, and chili flakes',
        'cuisine': 'Italian',
        'dietary': None,
        'ingredients': ['pasta', 'garlic', 'olive oil', 'chili flakes', 'salt', 'pepper']
    },
    {
        'recipe_id': 8,
        'title': 'Overnight Oats',
        'budget': 1.80,
        'cooking_time': 5,
        'description': 'Healthy breakfast prepared the night before with oats and fruits',
        'cuisine': None,
        'ingredients': ['oat', 'banana', 'strawberries', 'peanuts', 'sugar', 'salt']
    },
    {
        'recipe_id': 9,
        'title': 'Thai Green Curry',
        'budget': 8.50,
        'cooking_time': 45,
        'description': 'Spicy coconut curry with vegetables and your choice of protein',
        'cuisine': None,
        'dietary': None,
        'ingredients': ['beef', 'coconut curry sauce', 'carrots',
                        'onions', 'green onions', 'cabbage', 'garlic',
                        'chili pepper', 'tomatoes', 'soy sauce',
                        'red pepper flakes', 'sugar', 'salt']
    },
    {
        'recipe_id': 10,
        'title': 'Margherita Pizza',
        'budget': 5.00,
        'cooking_time': 25,
        'description': 'Classic Italian pizza with tomato, mozzarella, and basil',
        'cuisine': 'Italian',
        'dietary': None,
        'ingredients': ['pasta', 'tomatoes', 'mozzarella', 'basil', 'cheese', 'salt', 'pepper']
    },
    {
        'recipe_id': 11,
        'title': 'Mushroom Risotto',
        'budget': 6.00,
        'cooking_time': 40,
        'description': 'Creamy Italian rice dish with savory mushrooms',
        'cuisine': 'Italian',
        'dietary': None,
        'ingredients': ['rice', 'mushrooms', 'tomatoes', 'cheese', 'salt', 'pepper']
    },
    {
        'recipe_id': 12,
        'title': 'Avocado Egg Boats',
        'budget': 4.50,
        'cooking_time': 20,
        'description': 'Baked avocado halves filled with eggs and bacon',
        'cuisine': 'American',
        'dietary': 'gluten-free',
        'ingredients': ['avocado', 'eggs', 'bacon', 'cheese', 'herbs']
    },
    {
        'recipe_id': 13,
        'title': 'Mapo Tofu',
        'budget': 3.80,
        'cooking_time': 20,
        'description': 'Spicy Sichuan tofu dish with minced pork and fermented beans',
        'cuisine': 'Chinese',
        'dietary': None,
        'ingredients': ['tofu', 'ground pork', 'doubanjiang', 'sichuan peppercorns', 'green onions']
    },
    {
        'recipe_id': 14,
        'title': 'Beef Tacos',
        'budget': 5.50,
        'cooking_time': 20,
        'description': 'Mexican-style tacos with seasoned ground beef and fresh toppings',
        'cuisine': 'Mexican',
        'dietary': None,
        'ingredients': ['ground beef', 'onion', 'chili pepper', 'garlic', 'tomatoes', 'salt', 'pepper', 'taco']
    },
    {
        'recipe_id': 15,
        'title': 'Shrimp Fried Rice',
        'budget': 7.20,
        'cooking_time': 18,
        'description': 'Asian-style fried rice with succulent shrimp and vegetables',
        'cuisine': 'Chinese',
        'dietary': None,
        'ingredients': ['shrimp', 'rice', 'eggs', 'carrots', 'onions',
                        'cabbage', 'tomatoes', 'green onions', 'salt', 'pepper']
    },
]