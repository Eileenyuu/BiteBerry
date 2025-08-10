from fastapi import FastAPI, Depends, HTTPException
from typing import List
from database import init_db, get_db
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import crud
from schemas import UserPreferencesBase, UserPreferencesCreate, UserPreferencesUpdate, UserPreferencesResponse, UserCreate, UserLogin, UserResponse, RecipeResponse, LikeCreate, LikeResponse, RecipeLikeCount
from models import UserPreferences, User, DietaryRestriction, Recipe, Like
from config import DefaultPreferences
import logging
import auth
from contextlib import asynccontextmanager
from datetime import datetime
import json

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

@app.get('/recipes', response_model=List[RecipeResponse])
async def get_recipes(db: Session = Depends(get_db)):
    """Get all recipes"""
    try:
        recipes = db.query(Recipe).all()
        return [RecipeResponse.from_orm(recipe) for recipe in recipes]
    except Exception as e:
        logger.error(f"Error retrieving recipes: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve recipes")

@app.get('/api/recipes/{recipe_id}', response_model=RecipeResponse)
async def get_recipe_detail(recipe_id: int, db: Session = Depends(get_db)):
    """Get detailed information for a specific recipe"""
    try:
        recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()

        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")

        return RecipeResponse.from_orm(recipe)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving recipe {recipe_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve recipe")

# User preferences endpoints
def get_or_create_preferences(db: Session, user_id: int) -> UserPreferences:
    """Fetch User Preferences for specific user, if not exist, create default"""
    try:
        preferences = db.query(UserPreferences).filter(UserPreferences.user_id == user_id).first()
        if not preferences:
            logger.info(f"No preferences found for user {user_id}, creating default preferences")
            default_prefs = UserPreferences(
                user_id=user_id,
                max_budget=20.0,
                max_cooking_time=30,
                dietary_restrictions=DietaryRestriction.NONE
            )
            db.add(default_prefs)
            db.commit()
            db.refresh(default_prefs)
            preferences = default_prefs
        return preferences
    except Exception as e:
        logger.error(f"Error getting or creating preferences: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get('/api/preferences/{user_id}', response_model=UserPreferencesResponse)
async def get_preferences(user_id: int, db: Session = Depends(get_db)):
    """Get user preferences for specific user"""
    try:
        logger.info(f"Fetching preferences for user {user_id}")
        preferences = get_or_create_preferences(db, user_id)
        return preferences
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving preferences: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve preferences")

@app.put('/api/preferences/{user_id}', response_model=UserPreferencesResponse)
async def update_preferences(user_id: int, preferences: UserPreferencesUpdate, db: Session = Depends(get_db)):
    """Update user preferences for specific user"""
    try:
        logger.info(f"Updating preferences for user {user_id}: {preferences.model_dump()}")
        
        # Fetch or Create current preferences
        current_pref = get_or_create_preferences(db, user_id)

        # Update preferences
        if preferences.max_budget is not None:
            current_pref.max_budget = preferences.max_budget
        if preferences.max_cooking_time is not None:
            current_pref.max_cooking_time = preferences.max_cooking_time
        if preferences.dietary_restrictions is not None:
            current_pref.dietary_restrictions = preferences.dietary_restrictions
            
        current_pref.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(current_pref)
        
        logger.info(f"Successfully updated preferences for user {user_id}")
        return current_pref
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating preferences: {e}")
        raise HTTPException(status_code=500, detail="Failed to update preferences")

# Core function - recommendation
@app.get('/recommend/{user_id}')
async def recommend_recipe(user_id: int, max_budget: float = None, max_cooking_time: int = None, dietary_restrictions: str = None, db: Session = Depends(get_db)):
    """
    Get recipe recommendations based on budget and cooking time constraints.
    
    Parameters will be resolved in this priority order:
    1. Query parameters (if provided)
    2. User's saved preferences (from database)
    3. System default values
    """
    try:
        # Get user preferences from database
        user_preferences = get_or_create_preferences(db, user_id)
        
        # Validate query parameters first
        if max_budget is not None and max_budget <= 0:
            raise HTTPException(status_code=400, detail="Budget must be a positive value")
        if max_cooking_time is not None and max_cooking_time <= 0:
            raise HTTPException(status_code=400, detail="Cooking time must be a positive value")
        
        # Use provided parameters or fall back to stored preferences
        final_budget = max_budget if max_budget is not None else user_preferences.max_budget
        final_cooking_time = max_cooking_time if max_cooking_time is not None else user_preferences.max_cooking_time
        
        # Handle dietary restrictions parameter
        if dietary_restrictions is not None:
            try:
                final_dietary_restrictions = DietaryRestriction(dietary_restrictions)
            except ValueError:
                final_dietary_restrictions = user_preferences.dietary_restrictions
        else:
            final_dietary_restrictions = user_preferences.dietary_restrictions
        
        # Filter recipes based on constraints
        recommended_recipes = []
        recipes = db.query(Recipe).all()
        
        if recipes:  # Check if recipes exist
            for recipe in recipes:
                # Apply budget, time, and dietary restriction filters
                if (recipe.budget <= final_budget and 
                    recipe.cooking_time <= final_cooking_time and
                    (final_dietary_restrictions == DietaryRestriction.NONE or 
                     recipe.dietary_restrictions == final_dietary_restrictions)):
                    
                    # Get like information for this recipe
                    like_count = db.query(Like).filter(Like.recipe_id == recipe.id).count()
                    user_has_liked = db.query(Like).filter(
                        Like.user_id == user_id, 
                        Like.recipe_id == recipe.id
                    ).first() is not None
                    
                    # Parse JSON only once and handle errors gracefully
                    try:
                        ingredients = json.loads(recipe.ingredients) if recipe.ingredients else []
                    except (json.JSONDecodeError, TypeError):
                        ingredients = []
                        logger.warning(f"Invalid ingredients JSON for recipe {recipe.id}")
                    
                    try:
                        instructions = json.loads(recipe.instructions) if recipe.instructions else []
                    except (json.JSONDecodeError, TypeError):
                        instructions = []
                        logger.warning(f"Invalid instructions JSON for recipe {recipe.id}")
                    
                    # Convert to dict format for response (maintaining compatibility)
                    recipe_data = {
                        'recipe_id': recipe.id,  # Keep frontend compatibility
                        'title': recipe.title,
                        'budget': recipe.budget,
                        'cooking_time': recipe.cooking_time,
                        'description': recipe.description,
                        'cuisine': recipe.cuisine,
                        'dietary': recipe.dietary_restrictions.value,
                        'servings': recipe.servings,
                        'ingredients': ingredients,
                        'instructions': instructions,
                        'like_count': like_count,
                        'user_has_liked': user_has_liked
                    }
                    recommended_recipes.append(recipe_data)
        
        # Prepare response with proper structure
        response = {
            'filters': {
                'max_budget': final_budget,
                'max_cooking_time': final_cooking_time,
                'dietary_restrictions': final_dietary_restrictions.value
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

# Authentication endpoints
@app.post('/api/register', response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        logger.info(f"Registering new user: {user_data.username}")
        new_user = auth.create_user(db, user_data)
        logger.info(f"User registered successfully: {new_user.username}")
        return new_user
    except ValueError as e:
        logger.warning(f"Registration failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error during registration: {e}")
        raise HTTPException(status_code=500, detail="Registration failed")

@app.post('/api/login')
async def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """User login"""
    try:
        logger.info(f"Login attempt for user: {login_data.username}")
        user = auth.authenticate_user(db, login_data)
        logger.info(f"User logged in successfully: {user.username}")
        return {
            "message": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }
    except ValueError as e:
        logger.warning(f"Login failed: {e}")
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        logger.error(f"Error during login: {e}")
        raise HTTPException(status_code=500, detail="Login failed")

# Like endpoints
@app.post('/api/recipes/{recipe_id}/like/{user_id}', response_model=LikeResponse)
async def like_recipe(recipe_id: int, user_id: int, db: Session = Depends(get_db)):
    """Like a recipe (user can only like once)"""
    try:
        logger.info(f"User {user_id} attempting to like recipe {recipe_id}")
        
        # Check if recipe exists
        recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        
        # Check if user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if user already liked this recipe
        existing_like = db.query(Like).filter(
            Like.user_id == user_id, 
            Like.recipe_id == recipe_id
        ).first()
        
        if existing_like:
            # Already liked - just return the existing like
            logger.info(f"User {user_id} already liked recipe {recipe_id}")
            return existing_like
        
        # Create new like
        new_like = Like(
            user_id=user_id,
            recipe_id=recipe_id,
            created_at=datetime.utcnow()
        )
        
        db.add(new_like)
        db.commit()
        db.refresh(new_like)
        
        logger.info(f"User {user_id} successfully liked recipe {recipe_id}")
        return new_like
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error liking recipe: {e}")
        raise HTTPException(status_code=500, detail="Failed to like recipe")

@app.get('/api/recipes/{recipe_id}/likes/{user_id}', response_model=RecipeLikeCount)
async def get_recipe_like_info(recipe_id: int, user_id: int, db: Session = Depends(get_db)):
    """Get like count for a recipe and whether current user has liked it"""
    try:
        # Check if recipe exists
        recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        
        # Count total likes for this recipe
        like_count = db.query(Like).filter(Like.recipe_id == recipe_id).count()
        
        # Check if current user has liked this recipe
        user_has_liked = db.query(Like).filter(
            Like.user_id == user_id, 
            Like.recipe_id == recipe_id
        ).first() is not None
        
        return RecipeLikeCount(
            recipe_id=recipe_id,
            like_count=like_count,
            user_has_liked=user_has_liked
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting like info: {e}")
        raise HTTPException(status_code=500, detail="Failed to get like information")

@app.delete('/api/recipes/{recipe_id}/unlike/{user_id}')
async def unlike_recipe(recipe_id: int, user_id: int, db: Session = Depends(get_db)):
    """Unlike a recipe (remove like)"""
    try:
        logger.info(f"User {user_id} attempting to unlike recipe {recipe_id}")
        
        # Check if recipe exists
        recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        
        # Find the existing like
        existing_like = db.query(Like).filter(
            Like.user_id == user_id, 
            Like.recipe_id == recipe_id
        ).first()
        
        if not existing_like:
            # User hasn't liked this recipe
            raise HTTPException(status_code=404, detail="Like not found")
        
        # Delete the like
        db.delete(existing_like)
        db.commit()
        
        logger.info(f"User {user_id} successfully unliked recipe {recipe_id}")
        return {"message": "Recipe unliked successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error unliking recipe: {e}")
        raise HTTPException(status_code=500, detail="Failed to unlike recipe")