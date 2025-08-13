"""
BiteBerry API - Main application entry point
Streamlined and organized backend structure
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

# Import core modules
from core.database import init_db

# Import API routes
from api.routes import recipes, auth, preferences, likes, shopping, meal_planning

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up BiteBerry API...")
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down BiteBerry API...")


app = FastAPI(
    title="BiteBerry API",
    description="Recipe recommendation system with user preferences",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Frontend dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get('/')
async def root():
    return {
        'message': 'Welcome to BiteBerry API!',
        'version': '2.0.0',
        'status': 'healthy'
    }

# Legacy route for backward compatibility
@app.get('/recipes')
async def get_recipes_legacy():
    """Legacy endpoint - redirects to new structure"""
    from api.routes.recipes import get_all_recipes
    from core.database import get_db
    
    db = next(get_db())
    return await get_all_recipes(db)

# Legacy recommendation route for backward compatibility  
@app.get('/recommend/{user_id}')
async def recommend_recipe_legacy(user_id: int, max_budget: float = None, max_cooking_time: int = None, dietary_restrictions: str = None):
    """Legacy endpoint - redirects to new structure"""
    from api.routes.recipes import recommend_recipe
    from core.database import get_db
    
    db = next(get_db())
    return await recommend_recipe(user_id, max_budget, max_cooking_time, dietary_restrictions, db)

# Include all API routes
app.include_router(recipes.router)
app.include_router(auth.router)
app.include_router(preferences.router)
app.include_router(likes.router)
app.include_router(shopping.router)
app.include_router(meal_planning.router)

# Health check endpoint
@app.get('/health')
async def health_check():
    return {
        'status': 'healthy',
        'version': '2.0.0',
        'message': 'BiteBerry API is running'
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)