#!/usr/bin/env python3
"""
Database reset utility with sample data

Usage:
  python reset_db.py    # Reset database and create sample users
"""
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.models import Base, User, UserPreferences, DietaryRestriction, Recipe, DifficultyLevel, Like
from services.auth_service import hash_password
from datetime import datetime
import json

def reset_database():
    """Reset the database and populate with sample data"""
    db_file = "biteberry.db"
    
    # Remove existing database
    if os.path.exists(db_file):
        try:
            os.remove(db_file)
            print(f"✅ Database reset successfully! Deleted: {db_file}")
        except Exception as e:
            print(f"❌ Error deleting database: {e}")
            sys.exit(1)
    
    # Create new database with sample data
    create_sample_data()

def create_sample_data():
    """Create sample users and preferences"""
    print("📊 Creating sample data...")
    
    # Create database engine and session
    engine = create_engine("sqlite:///./biteberry.db", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Sample users with different preferences
        sample_users = [
            {
                "username": "alice", 
                "email": "alice@example.com", 
                "password": "password123",
                "max_budget": 15.0,
                "max_cooking_time": 30,
                "dietary_restrictions": DietaryRestriction.VEGETARIAN
            },
            {
                "username": "bob", 
                "email": "bob@example.com", 
                "password": "password123",
                "max_budget": 25.0,
                "max_cooking_time": 45,
                "dietary_restrictions": DietaryRestriction.NONE
            },
            {
                "username": "carol", 
                "email": "carol@example.com", 
                "password": "password123",
                "max_budget": 8.0,
                "max_cooking_time": 20,
                "dietary_restrictions": DietaryRestriction.VEGAN
            },
            {
                "username": "demo", 
                "email": "demo@example.com", 
                "password": "demo123",
                "max_budget": 12.0,
                "max_cooking_time": 25,
                "dietary_restrictions": DietaryRestriction.GLUTEN_FREE
            }
        ]
        
        for user_data in sample_users:
            # Create user
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                password_hash=hash_password(user_data["password"]),
                created_at=datetime.utcnow()
            )
            db.add(user)
            db.flush()  # Get the user ID
            
            # Create user preferences
            preferences = UserPreferences(
                user_id=user.id,
                max_budget=user_data["max_budget"],
                max_cooking_time=user_data["max_cooking_time"],
                dietary_restrictions=user_data["dietary_restrictions"],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(preferences)
            
            print(f"👤 Created user: {user_data['username']} (Budget: £{user_data['max_budget']}, Time: {user_data['max_cooking_time']}min, Diet: {user_data['dietary_restrictions'].value})")
        
        # Create sample recipes
        create_sample_recipes(db)
        
        db.commit()
        print(f"\n✅ Sample data created successfully!")
        print("\n🔑 Login credentials:")
        print("Username: alice    | Password: password123 | (Vegetarian, £15, 30min)")
        print("Username: bob      | Password: password123 | (No restrictions, £25, 45min)")
        print("Username: carol    | Password: password123 | (Vegan, £8, 20min)")
        print("Username: demo     | Password: demo123     | (Gluten-free, £12, 25min)")
        print("\nNow you can start the server:")
        print("uvicorn main:app --reload")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

def create_sample_recipes(db):
    """Create quality sample recipes for the database"""
    print("🍳 Creating sample recipes...")
    
    recipes_data = [
        {
            "title": "Chicken Teriyaki",
            "description": "Japanese-style glazed chicken with steamed rice",
            "ingredients": ["chicken breast", "soy sauce", "mirin", "sugar", "rice", "vegetable oil"],
            "instructions": [
                "Cut chicken breast into bite-sized pieces",
                "Mix soy sauce, mirin, and sugar in a bowl to make the glaze",
                "Heat oil in a pan over medium-high heat",
                "Cook chicken pieces for 5-6 minutes until golden",
                "Add the glaze and cook for 2-3 minutes until sticky",
                "Serve over steamed rice"
            ],
            "cooking_time": 25,
            "prep_time": 10,
            "difficulty": DifficultyLevel.EASY,
            "servings": 2,
            "budget": 6.00,
            "calories_per_serving": 420,
            "cuisine": "Japanese",
            "dietary_restrictions": DietaryRestriction.NONE,
            "image_url": "https://picsum.photos/400/300?random=1"
        },
        {
            "title": "French Omelette",
            "description": "Classic French breakfast with herbs and cheese",
            "ingredients": ["eggs", "butter", "fresh herbs", "gruyere cheese", "salt", "black pepper"],
            "instructions": [
                "Beat 3 eggs with salt and pepper in a bowl",
                "Heat butter in a non-stick pan over low heat",
                "Pour in eggs and gently stir with a fork",
                "Add herbs and cheese when eggs are almost set",
                "Fold omelette in half and slide onto plate"
            ],
            "cooking_time": 10,
            "prep_time": 5,
            "difficulty": DifficultyLevel.MEDIUM,
            "servings": 1,
            "budget": 3.00,
            "calories_per_serving": 320,
            "cuisine": "French",
            "dietary_restrictions": DietaryRestriction.NONE,
            "image_url": "https://picsum.photos/400/300?random=2"
        },
        {
            "title": "Veggie Burrito Bowl",
            "description": "Mexican-inspired bowl with beans, rice, and fresh salsa",
            "ingredients": ["black beans", "brown rice", "tomatoes", "red onion", "avocado", "lime", "cilantro", "cumin", "olive oil"],
            "instructions": [
                "Cook rice according to package instructions",
                "Heat black beans with cumin and a pinch of salt",
                "Dice tomatoes and red onion for fresh salsa",
                "Mix salsa ingredients with lime juice and olive oil",
                "Slice avocado just before serving",
                "Assemble bowl with rice, beans, salsa, and avocado"
            ],
            "cooking_time": 18,
            "prep_time": 15,
            "difficulty": DifficultyLevel.EASY,
            "servings": 2,
            "budget": 4.50,
            "calories_per_serving": 380,
            "cuisine": "Mexican",
            "dietary_restrictions": DietaryRestriction.VEGAN,
            "image_url": "https://picsum.photos/400/300?random=3"
        },
        {
            "title": "Simple Pasta Aglio e Olio",
            "description": "Italian pasta with garlic, olive oil, and chili flakes",
            "ingredients": ["spaghetti", "garlic", "extra virgin olive oil", "red chili flakes", "parsley", "parmesan cheese", "salt"],
            "instructions": [
                "Cook pasta in salted boiling water until al dente",
                "Slice garlic thinly while pasta cooks",
                "Heat olive oil in a large pan over medium heat",
                "Add garlic and chili flakes, cook until fragrant",
                "Add drained pasta with some pasta water",
                "Toss with parsley and parmesan, season with salt"
            ],
            "cooking_time": 15,
            "prep_time": 5,
            "difficulty": DifficultyLevel.EASY,
            "servings": 2,
            "budget": 2.50,
            "calories_per_serving": 350,
            "cuisine": "Italian",
            "dietary_restrictions": DietaryRestriction.NONE,
            "image_url": "https://picsum.photos/400/300?random=4"
        },
        {
            "title": "Thai Green Curry",
            "description": "Spicy coconut curry with vegetables and choice of protein",
            "ingredients": ["chicken thigh", "green curry paste", "coconut milk", "thai basil", "bell peppers", "bamboo shoots", "fish sauce", "palm sugar", "jasmine rice"],
            "instructions": [
                "Cut chicken into strips and vegetables into chunks",
                "Heat thick coconut milk in a pot until oil separates",
                "Add curry paste and fry for 2 minutes until fragrant",
                "Add chicken and cook for 5 minutes",
                "Add remaining coconut milk and bring to simmer",
                "Add vegetables and cook for 15 minutes",
                "Season with fish sauce and palm sugar",
                "Garnish with thai basil and serve with rice"
            ],
            "cooking_time": 35,
            "prep_time": 15,
            "difficulty": DifficultyLevel.MEDIUM,
            "servings": 4,
            "budget": 8.50,
            "calories_per_serving": 450,
            "cuisine": "Thai",
            "dietary_restrictions": DietaryRestriction.NONE,
            "image_url": "https://picsum.photos/400/300?random=5"
        },
        {
            "title": "Avocado Toast Supreme",
            "description": "Gourmet avocado toast with poached egg and everything seasoning",
            "ingredients": ["sourdough bread", "ripe avocado", "eggs", "everything bagel seasoning", "lemon juice", "olive oil", "salt", "cherry tomatoes"],
            "instructions": [
                "Toast sourdough bread until golden",
                "Mash avocado with lemon juice and salt",
                "Bring water to gentle boil for poaching eggs",
                "Crack egg into small bowl, create whirlpool in water",
                "Gently drop egg into water, cook for 3-4 minutes",
                "Spread avocado on toast, top with poached egg",
                "Sprinkle with everything seasoning and halved tomatoes"
            ],
            "cooking_time": 12,
            "prep_time": 8,
            "difficulty": DifficultyLevel.MEDIUM,
            "servings": 1,
            "budget": 4.00,
            "calories_per_serving": 380,
            "cuisine": "American",
            "dietary_restrictions": DietaryRestriction.NONE,
            "image_url": "https://picsum.photos/400/300?random=6"
        },
        {
            "title": "Mediterranean Quinoa Salad",
            "description": "Fresh and healthy quinoa salad with feta and olives",
            "ingredients": ["quinoa", "cucumber", "cherry tomatoes", "red onion", "kalamata olives", "feta cheese", "lemon juice", "olive oil", "oregano", "parsley"],
            "instructions": [
                "Rinse quinoa and cook according to package instructions",
                "Let quinoa cool completely",
                "Dice cucumber, halve cherry tomatoes, slice red onion",
                "Whisk lemon juice with olive oil and oregano",
                "Combine quinoa with vegetables and olives",
                "Add dressing and crumbled feta",
                "Garnish with fresh parsley before serving"
            ],
            "cooking_time": 20,
            "prep_time": 15,
            "difficulty": DifficultyLevel.EASY,
            "servings": 3,
            "budget": 6.50,
            "calories_per_serving": 320,
            "cuisine": "Mediterranean",
            "dietary_restrictions": DietaryRestriction.VEGETARIAN,
            "image_url": "https://picsum.photos/400/300?random=7"
        },
        {
            "title": "Korean Bibimbap",
            "description": "Mixed rice bowl with seasoned vegetables and gochujang",
            "ingredients": ["short grain rice", "carrots", "spinach", "bean sprouts", "shiitake mushrooms", "eggs", "gochujang", "sesame oil", "soy sauce", "garlic"],
            "instructions": [
                "Cook rice and keep warm",
                "Blanch spinach and bean sprouts separately, season with sesame oil",
                "Julienne carrots and sauté until tender",
                "Slice and sauté mushrooms with garlic",
                "Fry eggs sunny side up",
                "Arrange vegetables over rice in sections",
                "Top with fried egg and serve with gochujang"
            ],
            "cooking_time": 40,
            "prep_time": 20,
            "difficulty": DifficultyLevel.HARD,
            "servings": 2,
            "budget": 7.80,
            "calories_per_serving": 480,
            "cuisine": "Korean",
            "dietary_restrictions": DietaryRestriction.NONE,
            "image_url": "https://picsum.photos/400/300?random=8"
        },
        {
            "title": "Mushroom Risotto",
            "description": "Creamy Italian rice dish with wild mushrooms and parmesan",
            "ingredients": ["arborio rice", "mixed wild mushrooms", "vegetable stock", "white wine", "onion", "garlic", "parmesan cheese", "butter", "olive oil"],
            "instructions": [
                "Slice mushrooms and sauté until golden, set aside",
                "Keep stock warm in a separate pan",
                "Sauté diced onion and garlic in olive oil",
                "Add rice and toast for 2 minutes",
                "Add wine and stir until absorbed",
                "Add warm stock one ladle at a time, stirring constantly",
                "Continue for 18-20 minutes until rice is creamy",
                "Stir in mushrooms, butter, and parmesan"
            ],
            "cooking_time": 35,
            "prep_time": 15,
            "difficulty": DifficultyLevel.HARD,
            "servings": 3,
            "budget": 9.00,
            "calories_per_serving": 420,
            "cuisine": "Italian",
            "dietary_restrictions": DietaryRestriction.VEGETARIAN,
            "image_url": "https://picsum.photos/400/300?random=9"
        },
        {
            "title": "Quick Chicken Stir Fry",
            "description": "Fast and healthy stir fry with mixed vegetables",
            "ingredients": ["chicken breast", "broccoli", "bell peppers", "snap peas", "carrots", "ginger", "garlic", "soy sauce", "oyster sauce", "sesame oil"],
            "instructions": [
                "Cut chicken into thin strips",
                "Prepare all vegetables by cutting into bite-size pieces",
                "Heat oil in wok or large pan over high heat",
                "Stir fry chicken until nearly cooked through",
                "Add harder vegetables first (carrots, broccoli)",
                "Add remaining vegetables and stir fry for 2-3 minutes",
                "Add sauce mixture and toss everything together"
            ],
            "cooking_time": 15,
            "prep_time": 10,
            "difficulty": DifficultyLevel.EASY,
            "servings": 2,
            "budget": 5.50,
            "calories_per_serving": 290,
            "cuisine": "Asian",
            "dietary_restrictions": DietaryRestriction.NONE,
            "image_url": "https://picsum.photos/400/300?random=10"
        }
    ]
    
    for recipe_data in recipes_data:
        recipe = Recipe(
            title=recipe_data["title"],
            description=recipe_data["description"],
            ingredients=json.dumps(recipe_data["ingredients"]),
            instructions=json.dumps(recipe_data["instructions"]),
            cooking_time=recipe_data["cooking_time"],
            prep_time=recipe_data["prep_time"],
            difficulty=recipe_data["difficulty"],
            servings=recipe_data["servings"],
            budget=recipe_data["budget"],
            calories_per_serving=recipe_data["calories_per_serving"],
            cuisine=recipe_data["cuisine"],
            dietary_restrictions=recipe_data["dietary_restrictions"],
            image_url=recipe_data["image_url"],
            is_featured=0,
            average_rating=0.0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(recipe)
        print(f"🍽️  Created recipe: {recipe_data['title']} ({recipe_data['cuisine']}, £{recipe_data['budget']}, {recipe_data['cooking_time']}min)")

if __name__ == "__main__":
    print("🔄 Resetting database with sample data...")
    reset_database()