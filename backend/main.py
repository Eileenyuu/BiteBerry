from fastapi import FastAPI, Depends, HTTPException
from database import fake_recipes, init_db, get_db
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import crud
from schemas import UserPreferencesBase, UserPreferencesCreate, UserPreferencesUpdate, UserPreferencesResponse
from models import UserPreferences
from config import DefaultPreferences
import logging
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up BiteBerry API...")
    try:
        init_db()
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down BiteBerry API...")

app = FastAPI(lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Frontend dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get('/')
async def root():
    return {'message': 'Welcome to BiteBerry API!'}

@app.get('/recipes')
async def get_recipes():
    return fake_recipes

# User preferences endpoints
def get_or_create_preferences(db: Session) -> UserPreferences:
    """Fetch User Preferences, if not exist, create default"""
    try:
        preferences = db.query(UserPreferences).first()
        if not preferences:
            logger.info("No preferences found, creating default preferences")
            default_prefs = UserPreferencesCreate()
            preferences = crud.create_user_preferences(db, default_prefs)
        return preferences
    except Exception as e:
        logger.error(f"Error getting or creating preferences: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get('/api/preferences', response_model=UserPreferencesResponse)
async def get_preferences(db: Session = Depends(get_db)):
    """Get the current user preferences"""
    try:
        logger.info("Fetching user preferences")
        preferences = get_or_create_preferences(db)
        return preferences
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving preferences: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve preferences")

@app.put('/api/preferences', response_model=UserPreferencesResponse)
async def update_preferences(preferences: UserPreferencesUpdate, db: Session = Depends(get_db)):
    """Update user preferences"""
    try:
        logger.info(f"Updating preferences: {preferences.model_dump()}")
        
        # Fetch or Create current preferences
        current_pref = get_or_create_preferences(db)

        # Update preferences
        updated = crud.update_user_preferences(db, current_pref.id, preferences)

        if not updated:
            raise HTTPException(status_code=404, detail="Preferences not found")
        
        logger.info(f"Successfully updated preferences for ID: {current_pref.id}")
        return updated
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating preferences: {e}")
        raise HTTPException(status_code=500, detail="Failed to update preferences")

# Core function - recommendation
@app.get('/recommend')
async def recommend_recipe(max_budget: float = None, max_cooking_time: int = None, db: Session = Depends(get_db)):
    """
    Get recipe recommendations based on budget and cooking time constraints.
    
    Parameters will be resolved in this priority order:
    1. Query parameters (if provided)
    2. User's saved preferences (from database)
    3. System default values
    """
    try:
        # Get user preferences from database
        user_preferences = get_or_create_preferences(db)
        
        # Validate query parameters first
        if max_budget is not None and max_budget <= 0:
            raise HTTPException(status_code=400, detail="Budget must be a positive value")
        if max_cooking_time is not None and max_cooking_time <= 0:
            raise HTTPException(status_code=400, detail="Cooking time must be a positive value")
        
        # Use provided parameters or fall back to stored preferences
        final_budget = max_budget if max_budget is not None else user_preferences.max_budget
        final_cooking_time = max_cooking_time if max_cooking_time is not None else user_preferences.max_cooking_time
        
        # Filter recipes based on constraints
        recommended_recipes = []
        if fake_recipes:  # Check if recipes exist
            for recipe in fake_recipes:
                # Apply budget and time filters
                if (recipe.get('budget', 0) <= final_budget and 
                    recipe.get('cooking_time', 0) <= final_cooking_time):
                    recommended_recipes.append(recipe)
        
        # Prepare response with proper structure
        response = {
            'filters': {
                'max_budget': final_budget,
                'max_cooking_time': final_cooking_time,
                'dietary_restrictions': user_preferences.dietary_restrictions.value
            },
            'recommendations': recommended_recipes,
            'total_count': len(recommended_recipes)
        }
        
        # Add suggestion message if no results found
        if not recommended_recipes:
            response['message'] = "No recipes found matching your criteria. Try increasing your budget or cooking time."
        
        logger.info(f"Returning {len(recommended_recipes)} recommendations for budget=${final_budget}, time={final_cooking_time}min")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in recommend_recipe: {e}")
        raise HTTPException(status_code=500, detail="Failed to get recommendations")

