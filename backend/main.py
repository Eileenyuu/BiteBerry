from fastapi import FastAPI, Depends, HTTPException
from database import fake_recipes, init_db, get_db
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import crud
from schemas import UserPreferencesBase, UserPreferencesCreate, UserPreferencesUpdate, UserPreferencesResponse
from models import UserPreferences
import logging

app = FastAPI()

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    preferences = db.query(UserPreference).first()
    if not preferences:
        default_prefs = UserPreferencesCreate()
        preferences = crud.create_user_preferences(db, default_prefs)
    return preferences

@app.get('/preferences', response_model=UserPreferencesResponse)
async def get_preferences(db: Session = Depends(get_db)):
    """Get the current user preferences"""
    return get_or_create_preferences(db)

@app.put('/preferences', response_model=UserPreferencesResponse)
async def update_preferences(preferences: UserPreferencesBase, db: Session = Depends(get_db)):
    """Update user preferences"""
    # Fetch or Create
    current_pref = get_or_create_preferences(db)

    # Update
    prefs_update = UserPreferencesUpdate(**preferences.dict())
    updated = crud.update_user_preferences(db, current_pref.id, prefs_update)

    if not updated:
        raise HTTPException(status_code=404, detail="Preferences not found")
    return updated

# Core function - recommendation
@app.get('/recommend')
async def recommend_recipe(max_budget: float = None, max_cooking_time: int = None, db: Session = Depends(get_db)):
    # Get user preferences from database if query parameters are not provided
    user_preferences = db.query(UserPreferences).first()
    
    # Use provided parameters or fall back to stored preferences or defaults
    if max_budget is None:
        max_budget = user_preferences.max_budget if user_preferences else 50.0
    
    if max_cooking_time is None:
        max_cooking_time = user_preferences.max_cooking_time if user_preferences else 30
    
    recommended_recipe = []
    for recipe in fake_recipes:
        if recipe['budget'] <= max_budget and recipe['cooking_time'] <= max_cooking_time:
            recommended_recipe.append(recipe)

    return {
        'filters': {
            'max_budget': max_budget,
            'max_cooking_time': max_cooking_time
        },
        'recommendations': recommended_recipe
    }