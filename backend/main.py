from fastapi import FastAPI
from database import fake_recipes, init_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


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

# Core function - recommendation
@app.get('/recommend')
async def recommend_recipe(max_budget: float = 50.0, max_cooking_time: int = 30):
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