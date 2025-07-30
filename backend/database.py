from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import logging
import os

from models import Base, UserPreferences, DietaryRestriction

# Config logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Config SQLite database
# Use different database for testing
if os.getenv("TESTING") == "true":
    SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"  # In-memory database for testing
else:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./biteberry.db"

# Create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize the database by creating all tables."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
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
        'ingredients': ['chicken breast', 'soy sauce', 'mirin', 'sugar', 'rice'],
        'instructions': [
            'Cut chicken breast into bite-sized pieces',
            'Mix soy sauce, mirin, and sugar in a bowl to make the glaze',
            'Heat oil in a pan over medium-high heat',
            'Cook chicken pieces for 5-6 minutes until golden',
            'Add the glaze and cook for 2-3 minutes until sticky',
            'Serve over steamed rice'
        ],
        'servings': 2
    },
    {
        'recipe_id': 2,
        'title': 'French Omelette',
        'budget': 3.00,
        'cooking_time': 10,
        'description': 'Classic French breakfast with herbs and cheese',
        'cuisine': 'French',
        'dietary': None,
        'ingredients': ['eggs', 'butter', 'herbs', 'cheese', 'salt'],
        'instructions': [
            'Beat 3 eggs with salt in a bowl',
            'Heat butter in a non-stick pan over low heat',
            'Pour in eggs and gently stir with a fork',
            'Add herbs and cheese when eggs are almost set',
            'Fold omelette in half and slide onto plate'
        ],
        'servings': 1
    },
    {
        'recipe_id': 3,
        'title': 'BBQ Pulled Pork Burger',
        'budget': 7.80,
        'cooking_time': 25,
        'description': 'Tender pulled pork with tangy BBQ sauce on a soft bun',
        'cuisine': None,
        'dietary': None,
        'ingredients': ['pulled pork shoulder', 'grilled cheese', 'onion', 'salt'],
        'instructions': [
            'Heat pre-cooked pulled pork in a pan',
            'Add BBQ sauce and simmer for 5 minutes',
            'Toast burger buns until golden',
            'Slice onions and grill cheese',
            'Assemble burger with pork, cheese, and onions'
        ],
        'servings': 2
    },
    {
        'recipe_id': 4,
        'title': 'Char Siu Pork',
        'budget': 7.50,
        'cooking_time': 40,
        'description': 'Cantonese BBQ pork with sweet and savory glaze',
        'cuisine': 'Chinese',
        'dietary': None,
        'ingredients': ['pork shoulder', 'honey', 'hoisin sauce', 'five-spice', 'salt'],
        'instructions': [
            'Cut pork shoulder into long strips',
            'Mix honey, hoisin sauce, five-spice, and salt for marinade',
            'Marinate pork for 30 minutes',
            'Preheat oven to 200°C',
            'Roast pork for 25 minutes, basting every 10 minutes',
            'Let rest for 5 minutes before slicing'
        ],
        'servings': 3
    },
    {
        'recipe_id': 5,
        'title': 'Egg Fried Noodles',
        'budget': 3.50,
        'cooking_time': 15,
        'description': 'Quick Asian noodles with scrambled eggs and vegetables',
        'cuisine': None,
        'dietary': None,
        'ingredients': ['eggs', 'vegetables', 'noodles', 'salt'],
        'instructions': [
            'Cook noodles according to package instructions',
            'Beat eggs with salt',
            'Heat oil in wok or large pan',
            'Scramble eggs and set aside',
            'Stir-fry vegetables for 2 minutes',
            'Add noodles and eggs, toss everything together'
        ],
        'servings': 2
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
                        'sugar', 'olive oil', 'vinegar', 'salt'],
        'instructions': [
            'Cook rice according to package instructions',
            'Heat black beans with cumin and chili powder',
            'Dice onions and tomatoes for fresh salsa',
            'Mix salsa ingredients with olive oil and vinegar',
            'Season with salt, pepper, and sugar to taste',
            'Assemble bowl with rice, beans, and salsa'
        ],
        'servings': 2
    },
    {
        'recipe_id': 7,
        'title': 'Simple Pasta Aglio e Olio',
        'budget': 2.50,
        'cooking_time': 15,
        'description': 'Italian pasta with garlic, olive oil, and chili flakes',
        'cuisine': 'Italian',
        'dietary': None,
        'ingredients': ['pasta', 'garlic', 'olive oil', 'chili flakes', 'salt', 'pepper'],
        'instructions': [
            'Cook pasta in salted boiling water until al dente',
            'Slice garlic thinly',
            'Heat olive oil in a large pan',
            'Add garlic and chili flakes, cook until fragrant',
            'Add drained pasta to the pan',
            'Toss with pasta water, salt, and pepper'
        ],
        'servings': 2
    },
    {
        'recipe_id': 8,
        'title': 'Overnight Oats',
        'budget': 1.80,
        'cooking_time': 5,
        'description': 'Healthy breakfast prepared the night before with oats and fruits',
        'cuisine': None,
        'ingredients': ['oat', 'banana', 'strawberries', 'peanuts', 'sugar', 'salt'],
        'instructions': [
            'Mix oats with a pinch of salt and sugar in a jar',
            'Add enough milk to cover oats',
            'Slice banana and strawberries',
            'Layer fruits on top of oats',
            'Sprinkle peanuts on top',
            'Refrigerate overnight and enjoy in the morning'
        ],
        'servings': 1
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
                        'red pepper flakes', 'sugar', 'salt'],
        'instructions': [
            'Cut beef into strips and vegetables into chunks',
            'Heat oil in a large pot',
            'Brown beef for 5 minutes',
            'Add garlic, chili, and curry paste, cook for 2 minutes',
            'Add coconut milk and bring to simmer',
            'Add vegetables and cook for 20 minutes',
            'Season with soy sauce, sugar, and salt',
            'Garnish with green onions'
        ],
        'servings': 4
    },
    {
        'recipe_id': 10,
        'title': 'Margherita Pizza',
        'budget': 5.00,
        'cooking_time': 25,
        'description': 'Classic Italian pizza with tomato, mozzarella, and basil',
        'cuisine': 'Italian',
        'dietary': None,
        'ingredients': ['pasta', 'tomatoes', 'mozzarella', 'basil', 'cheese', 'salt', 'pepper'],
        'instructions': [
            'Preheat oven to 220°C',
            'Roll out pizza dough on floured surface',
            'Spread tomato sauce evenly on dough',
            'Tear mozzarella and distribute on pizza',
            'Season with salt and pepper',
            'Bake for 12-15 minutes until golden',
            'Top with fresh basil leaves before serving'
        ],
        'servings': 2
    },
    {
        'recipe_id': 11,
        'title': 'Mushroom Risotto',
        'budget': 6.00,
        'cooking_time': 40,
        'description': 'Creamy Italian rice dish with savory mushrooms',
        'cuisine': 'Italian',
        'dietary': None,
        'ingredients': ['rice', 'mushrooms', 'tomatoes', 'cheese', 'salt', 'pepper'],
        'instructions': [
            'Slice mushrooms and dice tomatoes',
            'Heat stock in a separate pan and keep warm',
            'Sauté mushrooms until golden, set aside',
            'Add rice to pan and toast for 2 minutes',
            'Add warm stock one ladle at a time, stirring constantly',
            'Continue for 18-20 minutes until rice is creamy',
            'Stir in mushrooms and cheese',
            'Season with salt and pepper'
        ],
        'servings': 3
    },
    {
        'recipe_id': 12,
        'title': 'Avocado Egg Boats',
        'budget': 4.50,
        'cooking_time': 20,
        'description': 'Baked avocado halves filled with eggs and bacon',
        'cuisine': 'American',
        'dietary': 'gluten-free',
        'ingredients': ['avocado', 'eggs', 'bacon', 'cheese', 'herbs'],
        'instructions': [
            'Preheat oven to 180°C',
            'Cut avocados in half and remove pits',
            'Scoop out some flesh to make room for eggs',
            'Cook bacon until crispy, then chop',
            'Crack an egg into each avocado half',
            'Top with bacon and cheese',
            'Bake for 15 minutes until eggs are set',
            'Garnish with herbs'
        ],
        'servings': 2
    },
    {
        'recipe_id': 13,
        'title': 'Mapo Tofu',
        'budget': 3.80,
        'cooking_time': 20,
        'description': 'Spicy Sichuan tofu dish with minced pork and fermented beans',
        'cuisine': 'Chinese',
        'dietary': None,
        'ingredients': ['tofu', 'ground pork', 'doubanjiang', 'sichuan peppercorns', 'green onions'],
        'instructions': [
            'Cut tofu into cubes and blanch in boiling water',
            'Heat oil in wok and cook ground pork until browned',
            'Add doubanjiang and cook until fragrant',
            'Add tofu and gently mix',
            'Add stock and simmer for 5 minutes',
            'Sprinkle with ground Sichuan peppercorns',
            'Garnish with chopped green onions'
        ],
        'servings': 2
    },
    {
        'recipe_id': 14,
        'title': 'Beef Tacos',
        'budget': 5.50,
        'cooking_time': 20,
        'description': 'Mexican-style tacos with seasoned ground beef and fresh toppings',
        'cuisine': 'Mexican',
        'dietary': None,
        'ingredients': ['ground beef', 'onion', 'chili pepper', 'garlic', 'tomatoes', 'salt', 'pepper', 'taco'],
        'instructions': [
            'Brown ground beef in a large pan',
            'Add diced onions and cook until soft',
            'Add minced garlic and chili pepper',
            'Season with salt and pepper',
            'Add diced tomatoes and simmer for 10 minutes',
            'Warm taco shells in oven',
            'Fill tacos with beef mixture and desired toppings'
        ],
        'servings': 3
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
                        'cabbage', 'tomatoes', 'green onions', 'salt', 'pepper'],
        'instructions': [
            'Cook rice and let it cool completely',
            'Clean and devein shrimp',
            'Dice all vegetables',
            'Beat eggs and scramble in wok, set aside',
            'Stir-fry shrimp until pink, set aside',
            'Stir-fry vegetables for 3 minutes',
            'Add rice and break up clumps',
            'Return eggs and shrimp to wok, toss everything together',
            'Season with salt and pepper, garnish with green onions'
        ],
        'servings': 3
    },
]