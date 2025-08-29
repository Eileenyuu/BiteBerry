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
        },
        {
            "title": "Gluten-Free Pancakes",
            "description": "Fluffy pancakes made with almond flour and fresh berries",
            "ingredients": ["almond flour", "eggs", "almond milk", "baking powder", "vanilla extract", "honey", "blueberries", "butter"],
            "instructions": [
                "Mix almond flour and baking powder in a bowl",
                "Whisk eggs, almond milk, vanilla, and honey separately",
                "Combine wet and dry ingredients until just mixed",
                "Heat butter in pan over medium heat",
                "Pour batter to form small pancakes",
                "Cook until bubbles form, flip and cook until golden",
                "Serve topped with fresh blueberries"
            ],
            "cooking_time": 15,
            "prep_time": 10,
            "difficulty": DifficultyLevel.EASY,
            "servings": 2,
            "budget": 5.00,
            "calories_per_serving": 320,
            "cuisine": "American",
            "dietary_restrictions": DietaryRestriction.GLUTEN_FREE,
            "image_url": "https://picsum.photos/400/300?random=11"
        },
        {
            "title": "Vegan Buddha Bowl",
            "description": "Nourishing bowl with roasted vegetables, quinoa, and tahini dressing",
            "ingredients": ["quinoa", "sweet potato", "chickpeas", "kale", "red cabbage", "tahini", "lemon juice", "maple syrup", "olive oil", "pumpkin seeds"],
            "instructions": [
                "Cook quinoa according to package instructions",
                "Cube sweet potato and roast at 400°F for 25 minutes",
                "Massage kale with a bit of oil and lemon",
                "Rinse and drain chickpeas, roast with sweet potato for last 15 minutes",
                "Whisk tahini, lemon juice, maple syrup, and water for dressing",
                "Thinly slice red cabbage",
                "Assemble bowl with quinoa, vegetables, and drizzle with dressing",
                "Top with pumpkin seeds"
            ],
            "cooking_time": 30,
            "prep_time": 15,
            "difficulty": DifficultyLevel.EASY,
            "servings": 2,
            "budget": 6.00,
            "calories_per_serving": 450,
            "cuisine": "Modern",
            "dietary_restrictions": DietaryRestriction.VEGAN,
            "image_url": "https://picsum.photos/400/300?random=12"
        },
        {
            "title": "Beef Tacos",
            "description": "Mexican street-style tacos with seasoned ground beef",
            "ingredients": ["ground beef", "corn tortillas", "white onion", "cilantro", "lime", "cumin", "chili powder", "garlic powder", "salt", "hot sauce"],
            "instructions": [
                "Brown ground beef in a large skillet",
                "Add cumin, chili powder, garlic powder, and salt",
                "Cook until beef is fully cooked and seasoned",
                "Warm tortillas in dry pan or microwave",
                "Dice onion finely and chop cilantro",
                "Fill tortillas with beef mixture",
                "Top with onion, cilantro, and lime juice",
                "Serve with hot sauce on the side"
            ],
            "cooking_time": 20,
            "prep_time": 10,
            "difficulty": DifficultyLevel.EASY,
            "servings": 3,
            "budget": 7.50,
            "calories_per_serving": 380,
            "cuisine": "Mexican",
            "dietary_restrictions": DietaryRestriction.NONE,
            "image_url": "https://picsum.photos/400/300?random=13"
        },
        {
            "title": "Coconut Curry Lentils",
            "description": "Warming Indian-style curry with red lentils and coconut milk",
            "ingredients": ["red lentils", "coconut milk", "onion", "garlic", "ginger", "turmeric", "cumin", "coriander", "tomatoes", "spinach", "basmati rice"],
            "instructions": [
                "Rinse lentils and cook in water until tender",
                "Cook basmati rice separately",
                "Sauté diced onion until translucent",
                "Add minced garlic and ginger, cook for 1 minute",
                "Add turmeric, cumin, and coriander, toast spices",
                "Add diced tomatoes and cook until soft",
                "Stir in cooked lentils and coconut milk",
                "Simmer for 10 minutes, add spinach in last 2 minutes",
                "Serve over rice"
            ],
            "cooking_time": 35,
            "prep_time": 10,
            "difficulty": DifficultyLevel.MEDIUM,
            "servings": 4,
            "budget": 4.50,
            "calories_per_serving": 380,
            "cuisine": "Indian",
            "dietary_restrictions": DietaryRestriction.VEGAN,
            "image_url": "https://picsum.photos/400/300?random=14"
        },
        {
            "title": "Caesar Salad",
            "description": "Classic Roman salad with homemade dressing and croutons",
            "ingredients": ["romaine lettuce", "bread", "parmesan cheese", "anchovies", "garlic", "lemon juice", "olive oil", "egg yolk", "worcestershire sauce"],
            "instructions": [
                "Cube bread and toast in oven until golden for croutons",
                "Wash and chop romaine lettuce",
                "Mash anchovies and garlic into a paste",
                "Whisk egg yolk with lemon juice",
                "Slowly add olive oil while whisking to make dressing",
                "Add anchovy paste and worcestershire to dressing",
                "Toss lettuce with dressing",
                "Top with croutons and grated parmesan"
            ],
            "cooking_time": 15,
            "prep_time": 15,
            "difficulty": DifficultyLevel.MEDIUM,
            "servings": 2,
            "budget": 4.00,
            "calories_per_serving": 280,
            "cuisine": "Italian",
            "dietary_restrictions": DietaryRestriction.NONE,
            "image_url": "https://picsum.photos/400/300?random=15"
        },
        {
            "title": "Dairy-Free Smoothie Bowl",
            "description": "Tropical smoothie bowl with coconut milk and fresh fruits",
            "ingredients": ["frozen mango", "frozen pineapple", "banana", "coconut milk", "chia seeds", "granola", "coconut flakes", "kiwi"],
            "instructions": [
                "Blend frozen mango, pineapple, half banana, and coconut milk until thick",
                "Pour smoothie into bowl",
                "Slice remaining banana and kiwi",
                "Arrange fruit slices on top of smoothie",
                "Sprinkle with chia seeds, granola, and coconut flakes",
                "Serve immediately while cold"
            ],
            "cooking_time": 5,
            "prep_time": 10,
            "difficulty": DifficultyLevel.EASY,
            "servings": 1,
            "budget": 3.50,
            "calories_per_serving": 350,
            "cuisine": "Modern",
            "dietary_restrictions": DietaryRestriction.DAIRY_FREE,
            "image_url": "https://picsum.photos/400/300?random=16"
        },
        {
            "title": "Salmon Teriyaki",
            "description": "Pan-seared salmon with homemade teriyaki glaze",
            "ingredients": ["salmon fillets", "soy sauce", "mirin", "sake", "sugar", "ginger", "garlic", "sesame oil", "green onions", "sesame seeds"],
            "instructions": [
                "Mix soy sauce, mirin, sake, and sugar for teriyaki sauce",
                "Grate ginger and mince garlic, add to sauce",
                "Heat sesame oil in pan over medium-high heat",
                "Season salmon and cook skin-side down for 4 minutes",
                "Flip salmon and cook 3 more minutes",
                "Add teriyaki sauce to pan and let it bubble",
                "Baste salmon with sauce until glazed",
                "Garnish with sliced green onions and sesame seeds"
            ],
            "cooking_time": 15,
            "prep_time": 10,
            "difficulty": DifficultyLevel.MEDIUM,
            "servings": 2,
            "budget": 12.00,
            "calories_per_serving": 420,
            "cuisine": "Japanese",
            "dietary_restrictions": DietaryRestriction.NONE,
            "image_url": "https://picsum.photos/400/300?random=17"
        },
        {
            "title": "Nut-Free Energy Balls",
            "description": "Healthy snack balls made with seeds and dried fruits",
            "ingredients": ["dates", "sunflower seeds", "pumpkin seeds", "dried cranberries", "coconut flakes", "vanilla extract", "cocoa powder"],
            "instructions": [
                "Pit dates and soak in warm water for 10 minutes",
                "Drain dates and add to food processor",
                "Add sunflower seeds, pumpkin seeds, and process until chunky",
                "Add dried cranberries, coconut, vanilla, and cocoa",
                "Process until mixture holds together when pressed",
                "Roll mixture into small balls with hands",
                "Chill in refrigerator for 30 minutes before serving"
            ],
            "cooking_time": 5,
            "prep_time": 20,
            "difficulty": DifficultyLevel.EASY,
            "servings": 4,
            "budget": 3.00,
            "calories_per_serving": 180,
            "cuisine": "Modern",
            "dietary_restrictions": DietaryRestriction.NUT_FREE,
            "image_url": "https://picsum.photos/400/300?random=18"
        },
        {
            "title": "Keto Zucchini Lasagna",
            "description": "Low-carb lasagna using zucchini slices instead of pasta",
            "ingredients": ["large zucchini", "ground turkey", "ricotta cheese", "mozzarella cheese", "parmesan cheese", "eggs", "marinara sauce", "italian seasoning", "garlic"],
            "instructions": [
                "Slice zucchini lengthwise into thin strips",
                "Salt zucchini strips and let drain for 30 minutes",
                "Brown ground turkey with garlic and italian seasoning",
                "Mix ricotta with eggs and half the mozzarella",
                "Pat zucchini dry with paper towels",
                "Layer zucchini, meat sauce, and cheese mixture",
                "Repeat layers, ending with mozzarella and parmesan",
                "Bake at 375°F for 45 minutes until bubbly"
            ],
            "cooking_time": 45,
            "prep_time": 30,
            "difficulty": DifficultyLevel.MEDIUM,
            "servings": 6,
            "budget": 9.50,
            "calories_per_serving": 320,
            "cuisine": "Italian",
            "dietary_restrictions": DietaryRestriction.KETO,
            "image_url": "https://picsum.photos/400/300?random=19"
        },
        {
            "title": "Paleo Chicken Wings",
            "description": "Crispy baked chicken wings with herbs and spices",
            "ingredients": ["chicken wings", "olive oil", "paprika", "garlic powder", "onion powder", "thyme", "rosemary", "salt", "black pepper", "lemon"],
            "instructions": [
                "Pat chicken wings completely dry",
                "Mix all spices and herbs in a bowl",
                "Toss wings with olive oil and spice mixture",
                "Let marinate for 30 minutes at room temperature",
                "Preheat oven to 425°F",
                "Arrange wings on baking sheet in single layer",
                "Bake for 45-50 minutes until skin is crispy",
                "Squeeze fresh lemon juice before serving"
            ],
            "cooking_time": 50,
            "prep_time": 15,
            "difficulty": DifficultyLevel.EASY,
            "servings": 3,
            "budget": 8.00,
            "calories_per_serving": 380,
            "cuisine": "American",
            "dietary_restrictions": DietaryRestriction.PALEO,
            "image_url": "https://picsum.photos/400/300?random=20"
        },
        {
            "title": "Spanish Paella",
            "description": "Traditional saffron rice dish with seafood and chicken",
            "ingredients": ["bomba rice", "saffron", "chicken thighs", "prawns", "mussels", "green beans", "garrofó beans", "tomato", "olive oil", "chicken stock", "lemon"],
            "instructions": [
                "Heat olive oil in paella pan over medium heat",
                "Season and brown chicken pieces, set aside",
                "Grate tomato and cook until reduced",
                "Add rice and toast for 2-3 minutes",
                "Add hot saffron stock, don't stir after this point",
                "Add chicken back, arrange seafood on top",
                "Add green beans and garrofó beans",
                "Cook for 20-25 minutes without stirring",
                "Rest for 5 minutes before serving with lemon"
            ],
            "cooking_time": 45,
            "prep_time": 20,
            "difficulty": DifficultyLevel.HARD,
            "servings": 6,
            "budget": 15.00,
            "calories_per_serving": 520,
            "cuisine": "Spanish",
            "dietary_restrictions": DietaryRestriction.NONE,
            "image_url": "https://picsum.photos/400/300?random=21"
        },
        {
            "title": "Greek Moussaka",
            "description": "Layered casserole with eggplant, meat sauce, and béchamel",
            "ingredients": ["eggplant", "ground lamb", "onions", "tomatoes", "red wine", "cinnamon", "butter", "flour", "milk", "parmesan", "nutmeg", "olive oil"],
            "instructions": [
                "Slice eggplant, salt and let drain for 30 minutes",
                "Pat dry and brush with olive oil, grill until golden",
                "Make meat sauce: brown lamb with onions",
                "Add tomatoes, wine, and cinnamon, simmer 20 minutes",
                "Make béchamel: melt butter, add flour, gradually whisk in milk",
                "Season béchamel with nutmeg and parmesan",
                "Layer eggplant, meat sauce, repeat, top with béchamel",
                "Bake at 350°F for 45 minutes until golden"
            ],
            "cooking_time": 60,
            "prep_time": 45,
            "difficulty": DifficultyLevel.HARD,
            "servings": 8,
            "budget": 12.50,
            "calories_per_serving": 480,
            "cuisine": "Greek",
            "dietary_restrictions": DietaryRestriction.NONE,
            "image_url": "https://picsum.photos/400/300?random=22"
        },
        {
            "title": "Chinese Kung Pao Chicken",
            "description": "Spicy Sichuan stir-fry with peanuts and dried chilies",
            "ingredients": ["chicken breast", "roasted peanuts", "dried red chilies", "sichuan peppercorns", "soy sauce", "rice wine", "sugar", "cornstarch", "ginger", "garlic", "scallions"],
            "instructions": [
                "Cut chicken into cubes and marinate with soy sauce and cornstarch",
                "Toast sichuan peppercorns and grind coarsely",
                "Heat oil in wok, fry dried chilies until fragrant",
                "Add chicken and stir-fry until nearly cooked",
                "Add ginger, garlic, and ground peppercorns",
                "Add sauce mixture and peanuts",
                "Toss quickly until sauce coats everything",
                "Garnish with sliced scallions"
            ],
            "cooking_time": 15,
            "prep_time": 20,
            "difficulty": DifficultyLevel.MEDIUM,
            "servings": 3,
            "budget": 7.00,
            "calories_per_serving": 340,
            "cuisine": "Chinese",
            "dietary_restrictions": DietaryRestriction.NONE,
            "image_url": "https://picsum.photos/400/300?random=23"
        },
        {
            "title": "Moroccan Tagine",
            "description": "Slow-cooked stew with lamb, apricots, and warm spices",
            "ingredients": ["lamb shoulder", "dried apricots", "onions", "cinnamon", "ginger", "turmeric", "saffron", "almonds", "honey", "preserved lemons", "cilantro", "couscous"],
            "instructions": [
                "Cut lamb into chunks and season with spices",
                "Brown lamb in tagine or heavy pot",
                "Add sliced onions and cook until soft",
                "Add saffron, preserved lemons, and water",
                "Cover and simmer for 1.5 hours",
                "Add apricots and honey, cook 30 more minutes",
                "Toast almonds until golden",
                "Serve over couscous, garnish with almonds and cilantro"
            ],
            "cooking_time": 120,
            "prep_time": 20,
            "difficulty": DifficultyLevel.HARD,
            "servings": 6,
            "budget": 14.00,
            "calories_per_serving": 520,
            "cuisine": "Moroccan",
            "dietary_restrictions": DietaryRestriction.NONE,
            "image_url": "https://picsum.photos/400/300?random=24"
        },
        {
            "title": "Brazilian Moqueca",
            "description": "Coconut fish stew with bell peppers and dendê oil",
            "ingredients": ["white fish fillets", "coconut milk", "dendê oil", "bell peppers", "onions", "tomatoes", "lime", "cilantro", "malagueta peppers", "cassava flour"],
            "instructions": [
                "Cut fish into chunks and marinate with lime and salt",
                "Slice bell peppers and onions",
                "Heat dendê oil in clay pot or heavy pan",
                "Sauté onions and peppers until soft",
                "Add diced tomatoes and cook until broken down",
                "Add coconut milk and bring to gentle simmer",
                "Add fish and malagueta peppers",
                "Cook 10 minutes until fish is flaky",
                "Thicken with cassava flour if needed, garnish with cilantro"
            ],
            "cooking_time": 25,
            "prep_time": 15,
            "difficulty": DifficultyLevel.MEDIUM,
            "servings": 4,
            "budget": 10.00,
            "calories_per_serving": 320,
            "cuisine": "Brazilian",
            "dietary_restrictions": DietaryRestriction.NONE,
            "image_url": "https://picsum.photos/400/300?random=25"
        },
        {
            "title": "Lebanese Tabbouleh",
            "description": "Fresh parsley salad with bulgur, tomatoes, and lemon",
            "ingredients": ["bulgur wheat", "fresh parsley", "mint", "tomatoes", "cucumber", "scallions", "lemon juice", "olive oil", "salt", "allspice"],
            "instructions": [
                "Soak bulgur in hot water for 30 minutes until tender",
                "Drain and squeeze out excess water",
                "Finely chop parsley, mint, and scallions",
                "Dice tomatoes and cucumber, removing seeds",
                "Mix bulgur with chopped herbs and vegetables",
                "Whisk lemon juice with olive oil, salt, and allspice",
                "Toss salad with dressing and let marinate 1 hour",
                "Adjust seasoning before serving"
            ],
            "cooking_time": 5,
            "prep_time": 30,
            "difficulty": DifficultyLevel.EASY,
            "servings": 4,
            "budget": 3.50,
            "calories_per_serving": 140,
            "cuisine": "Lebanese",
            "dietary_restrictions": DietaryRestriction.VEGAN,
            "image_url": "https://picsum.photos/400/300?random=26"
        },
        {
            "title": "German Schnitzel",
            "description": "Crispy breaded pork cutlets with lemon and herbs",
            "ingredients": ["pork loin", "flour", "eggs", "breadcrumbs", "butter", "lemon", "parsley", "salt", "black pepper", "vegetable oil"],
            "instructions": [
                "Pound pork cutlets to 1/4 inch thickness",
                "Season with salt and pepper",
                "Set up breading station: flour, beaten eggs, breadcrumbs",
                "Dredge cutlets in flour, then egg, then breadcrumbs",
                "Heat oil and butter in large skillet",
                "Fry schnitzels 3-4 minutes per side until golden",
                "Drain on paper towels",
                "Serve immediately with lemon wedges and parsley"
            ],
            "cooking_time": 15,
            "prep_time": 20,
            "difficulty": DifficultyLevel.MEDIUM,
            "servings": 4,
            "budget": 8.50,
            "calories_per_serving": 420,
            "cuisine": "German",
            "dietary_restrictions": DietaryRestriction.NONE,
            "image_url": "https://picsum.photos/400/300?random=27"
        },
        {
            "title": "Ethiopian Doro Wat",
            "description": "Spicy chicken stew with berbere spice and hard-boiled eggs",
            "ingredients": ["chicken pieces", "hard-boiled eggs", "red onions", "berbere spice", "garlic", "ginger", "tomato paste", "red wine", "clarified butter", "cardamom"],
            "instructions": [
                "Slowly cook diced onions until caramelized, about 45 minutes",
                "Add garlic, ginger, and berbere spice, cook 2 minutes",
                "Add tomato paste and cook until darkened",
                "Add red wine and simmer until reduced",
                "Add chicken pieces and enough water to cover",
                "Simmer 30 minutes until chicken is tender",
                "Add clarified butter and cardamom",
                "Add peeled hard-boiled eggs in last 10 minutes",
                "Serve with injera bread"
            ],
            "cooking_time": 90,
            "prep_time": 20,
            "difficulty": DifficultyLevel.HARD,
            "servings": 6,
            "budget": 9.00,
            "calories_per_serving": 480,
            "cuisine": "Ethiopian",
            "dietary_restrictions": DietaryRestriction.NONE,
            "image_url": "https://picsum.photos/400/300?random=28"
        },
        {
            "title": "Russian Borscht",
            "description": "Hearty beet soup with cabbage and sour cream",
            "ingredients": ["fresh beets", "beef broth", "cabbage", "carrots", "onions", "tomato paste", "garlic", "bay leaves", "dill", "sour cream", "potatoes"],
            "instructions": [
                "Roast whole beets at 400°F for 1 hour until tender",
                "Peel and grate roasted beets",
                "Sauté diced onions and carrots until soft",
                "Add tomato paste and cook 2 minutes",
                "Add grated beets and beef broth",
                "Add diced potatoes and bay leaves",
                "Simmer 20 minutes, add shredded cabbage",
                "Cook 10 more minutes, season with salt and pepper",
                "Serve hot with sour cream and fresh dill"
            ],
            "cooking_time": 45,
            "prep_time": 75,
            "difficulty": DifficultyLevel.MEDIUM,
            "servings": 6,
            "budget": 5.50,
            "calories_per_serving": 180,
            "cuisine": "Russian",
            "dietary_restrictions": DietaryRestriction.NONE,
            "image_url": "https://picsum.photos/400/300?random=29"
        },
        {
            "title": "Turkish Köfte",
            "description": "Spiced ground meat balls with yogurt sauce",
            "ingredients": ["ground lamb", "ground beef", "onion", "garlic", "parsley", "cumin", "paprika", "breadcrumbs", "egg", "greek yogurt", "cucumber", "mint", "sumac"],
            "instructions": [
                "Grate onion and squeeze out excess moisture",
                "Mix ground meats with onion, garlic, herbs, and spices",
                "Add breadcrumbs and egg, mix well",
                "Form into small oval patties",
                "Chill for 30 minutes to firm up",
                "Grill or pan-fry köfte until browned and cooked through",
                "Make yogurt sauce with grated cucumber and mint",
                "Serve köfte with yogurt sauce and sumac"
            ],
            "cooking_time": 15,
            "prep_time": 45,
            "difficulty": DifficultyLevel.MEDIUM,
            "servings": 4,
            "budget": 7.50,
            "calories_per_serving": 380,
            "cuisine": "Turkish",
            "dietary_restrictions": DietaryRestriction.NONE,
            "image_url": "https://picsum.photos/400/300?random=30"
        },
        {
            "title": "Vietnamese Pho",
            "description": "Aromatic beef noodle soup with herbs and spices",
            "ingredients": ["beef bones", "beef brisket", "rice noodles", "onions", "ginger", "star anise", "cinnamon", "cloves", "fish sauce", "bean sprouts", "thai basil", "lime"],
            "instructions": [
                "Char onions and ginger over open flame until blackened",
                "Toast whole spices in dry pan until fragrant",
                "Simmer beef bones and brisket for 3 hours",
                "Add charred vegetables and spices, simmer 1 more hour",
                "Strain broth and season with fish sauce",
                "Slice brisket thinly when cool enough to handle",
                "Cook rice noodles according to package instructions",
                "Serve hot broth over noodles with beef and herbs"
            ],
            "cooking_time": 240,
            "prep_time": 30,
            "difficulty": DifficultyLevel.HARD,
            "servings": 6,
            "budget": 11.00,
            "calories_per_serving": 420,
            "cuisine": "Vietnamese",
            "dietary_restrictions": DietaryRestriction.NONE,
            "image_url": "https://picsum.photos/400/300?random=31"
        },
        {
            "title": "Polish Pierogi",
            "description": "Dumplings filled with potato and cheese, served with sour cream",
            "ingredients": ["flour", "eggs", "potatoes", "cottage cheese", "onions", "butter", "sour cream", "chives", "salt", "black pepper"],
            "instructions": [
                "Make dough with flour, eggs, and water, let rest 1 hour",
                "Boil and mash potatoes, mix with cottage cheese",
                "Season filling with salt, pepper, and sautéed onions",
                "Roll dough thin and cut into circles",
                "Place filling in center, fold and seal edges",
                "Boil pierogi until they float, about 3-4 minutes",
                "Sauté boiled pierogi in butter until golden",
                "Serve with sour cream and chives"
            ],
            "cooking_time": 30,
            "prep_time": 90,
            "difficulty": DifficultyLevel.HARD,
            "servings": 6,
            "budget": 4.00,
            "calories_per_serving": 320,
            "cuisine": "Polish",
            "dietary_restrictions": DietaryRestriction.VEGETARIAN,
            "image_url": "https://picsum.photos/400/300?random=32"
        },
        {
            "title": "Jamaican Jerk Chicken",
            "description": "Spicy grilled chicken with Caribbean jerk seasoning",
            "ingredients": ["chicken thighs", "scotch bonnet peppers", "allspice", "thyme", "garlic", "ginger", "lime juice", "brown sugar", "soy sauce", "vegetable oil", "cinnamon"],
            "instructions": [
                "Make jerk marinade by blending peppers, spices, and aromatics",
                "Score chicken skin and rub marinade all over",
                "Marinate at least 2 hours or overnight",
                "Preheat grill to medium-high heat",
                "Grill chicken skin-side down first",
                "Cook 6-8 minutes per side, moving if flare-ups occur",
                "Check internal temperature reaches 165°F",
                "Rest 5 minutes before serving with lime wedges"
            ],
            "cooking_time": 20,
            "prep_time": 15,
            "difficulty": DifficultyLevel.MEDIUM,
            "servings": 4,
            "budget": 6.50,
            "calories_per_serving": 380,
            "cuisine": "Jamaican",
            "dietary_restrictions": DietaryRestriction.NONE,
            "image_url": "https://picsum.photos/400/300?random=33"
        },
        {
            "title": "Swedish Meatballs",
            "description": "Classic meatballs in cream sauce with lingonberry jam",
            "ingredients": ["ground beef", "ground pork", "breadcrumbs", "milk", "egg", "onion", "butter", "flour", "beef broth", "heavy cream", "lingonberry jam", "allspice"],
            "instructions": [
                "Soak breadcrumbs in milk until soft",
                "Mix ground meats with soaked breadcrumbs, egg, and grated onion",
                "Season with salt, pepper, and allspice",
                "Form into small, uniform meatballs",
                "Brown meatballs in butter in batches",
                "Make cream sauce with pan drippings, flour, and broth",
                "Add cream and return meatballs to pan",
                "Simmer 10 minutes, serve with lingonberry jam"
            ],
            "cooking_time": 30,
            "prep_time": 20,
            "difficulty": DifficultyLevel.MEDIUM,
            "servings": 4,
            "budget": 8.00,
            "calories_per_serving": 450,
            "cuisine": "Swedish",
            "dietary_restrictions": DietaryRestriction.NONE,
            "image_url": "https://picsum.photos/400/300?random=34"
        },
        {
            "title": "Peruvian Ceviche",
            "description": "Fresh fish 'cooked' in citrus juice with onions and peppers",
            "ingredients": ["white fish fillets", "lime juice", "lemon juice", "red onion", "aji amarillo peppers", "cilantro", "sweet potato", "corn", "salt", "black pepper"],
            "instructions": [
                "Cut fish into small cubes, removing any bones",
                "Slice red onion very thinly and rinse in cold water",
                "Mix lime and lemon juice in a bowl",
                "Add fish to citrus juice and marinate 15-20 minutes",
                "Fish should turn opaque when 'cooked'",
                "Add sliced onions, peppers, and cilantro",
                "Season with salt and pepper",
                "Serve immediately with boiled sweet potato and corn"
            ],
            "cooking_time": 0,
            "prep_time": 30,
            "difficulty": DifficultyLevel.EASY,
            "servings": 3,
            "budget": 9.00,
            "calories_per_serving": 220,
            "cuisine": "Peruvian",
            "dietary_restrictions": DietaryRestriction.NONE,
            "image_url": "https://picsum.photos/400/300?random=35"
        },
        {
            "title": "Hungarian Goulash",
            "description": "Hearty beef stew with paprika and vegetables",
            "ingredients": ["beef chuck", "onions", "hungarian paprika", "tomatoes", "bell peppers", "potatoes", "caraway seeds", "beef broth", "sour cream", "marjoram"],
            "instructions": [
                "Cut beef into large chunks and season",
                "Brown beef in batches in heavy pot",
                "Sauté sliced onions until caramelized",
                "Add paprika and cook for 1 minute",
                "Add tomatoes, peppers, and beef back to pot",
                "Add enough broth to cover, bring to simmer",
                "Cook covered for 1.5 hours until beef is tender",
                "Add diced potatoes in last 30 minutes",
                "Serve with a dollop of sour cream"
            ],
            "cooking_time": 120,
            "prep_time": 20,
            "difficulty": DifficultyLevel.MEDIUM,
            "servings": 6,
            "budget": 10.50,
            "calories_per_serving": 380,
            "cuisine": "Hungarian",
            "dietary_restrictions": DietaryRestriction.NONE,
            "image_url": "https://picsum.photos/400/300?random=36"
        },
        {
            "title": "Argentine Empanadas",
            "description": "Baked pastries filled with seasoned beef and onions",
            "ingredients": ["flour", "lard", "beef mince", "onions", "hard-boiled eggs", "green olives", "cumin", "paprika", "raisins", "egg wash"],
            "instructions": [
                "Make pastry dough with flour, lard, and water",
                "Rest dough for 30 minutes wrapped in plastic",
                "Cook beef with onions, cumin, and paprika until browned",
                "Cool filling completely before assembling",
                "Add chopped eggs, olives, and raisins to filling",
                "Roll dough and cut into circles",
                "Fill circles, fold and crimp edges to seal",
                "Brush with egg wash and bake at 375°F for 25 minutes"
            ],
            "cooking_time": 25,
            "prep_time": 60,
            "difficulty": DifficultyLevel.MEDIUM,
            "servings": 6,
            "budget": 6.00,
            "calories_per_serving": 320,
            "cuisine": "Argentine",
            "dietary_restrictions": DietaryRestriction.NONE,
            "image_url": "https://picsum.photos/400/300?random=37"
        },
        {
            "title": "Dutch Stroopwafels",
            "description": "Thin waffles filled with caramel syrup",
            "ingredients": ["flour", "butter", "brown sugar", "eggs", "yeast", "milk", "cinnamon", "golden syrup", "vanilla"],
            "instructions": [
                "Make waffle batter with flour, melted butter, sugar, and egg",
                "Add warm milk with dissolved yeast",
                "Let batter rest for 1 hour until bubbly",
                "Make caramel filling with brown sugar and golden syrup",
                "Cook thin waffles in stroopwafel iron",
                "While still warm, slice each waffle horizontally",
                "Spread caramel filling between layers",
                "Press together gently and let cool"
            ],
            "cooking_time": 30,
            "prep_time": 75,
            "difficulty": DifficultyLevel.HARD,
            "servings": 8,
            "budget": 4.50,
            "calories_per_serving": 280,
            "cuisine": "Dutch",
            "dietary_restrictions": DietaryRestriction.VEGETARIAN,
            "image_url": "https://picsum.photos/400/300?random=38"
        },
        {
            "title": "Nigerian Jollof Rice",
            "description": "Spiced one-pot rice dish with tomatoes and peppers",
            "ingredients": ["long grain rice", "tomatoes", "red bell peppers", "onions", "scotch bonnet peppers", "chicken stock", "tomato paste", "bay leaves", "thyme", "curry powder", "ginger", "garlic"],
            "instructions": [
                "Blend tomatoes, peppers, and onions into smooth paste",
                "Heat oil and fry tomato paste until oil separates",
                "Add blended mixture and cook until reduced by half",
                "Add spices, ginger, and garlic, cook 2 minutes",
                "Add rice and stir to coat with sauce",
                "Add hot chicken stock to cover rice by 1 inch",
                "Bring to boil, then reduce heat and cover",
                "Simmer 15-20 minutes until rice is tender",
                "Let rest 10 minutes before fluffing"
            ],
            "cooking_time": 35,
            "prep_time": 20,
            "difficulty": DifficultyLevel.MEDIUM,
            "servings": 6,
            "budget": 5.00,
            "calories_per_serving": 340,
            "cuisine": "Nigerian",
            "dietary_restrictions": DietaryRestriction.NONE,
            "image_url": "https://picsum.photos/400/300?random=39"
        },
        {
            "title": "Australian Meat Pies",
            "description": "Flaky pastry pies filled with seasoned ground beef",
            "ingredients": ["puff pastry", "ground beef", "onions", "beef stock", "worcestershire sauce", "tomato sauce", "flour", "egg wash", "thyme", "bay leaves"],
            "instructions": [
                "Brown ground beef with diced onions",
                "Sprinkle flour over meat and cook 2 minutes",
                "Add stock, worcestershire, tomato sauce, and herbs",
                "Simmer until thickened, about 15 minutes",
                "Cool filling completely",
                "Line pie tins with pastry, fill with meat mixture",
                "Top with pastry lids and crimp edges",
                "Brush with egg wash and bake at 400°F for 25 minutes"
            ],
            "cooking_time": 25,
            "prep_time": 30,
            "difficulty": DifficultyLevel.MEDIUM,
            "servings": 6,
            "budget": 7.00,
            "calories_per_serving": 420,
            "cuisine": "Australian",
            "dietary_restrictions": DietaryRestriction.NONE,
            "image_url": "https://picsum.photos/400/300?random=40"
        },
        {
            "title": "Scottish Haggis",
            "description": "Traditional pudding with oats, spices, and organ meat",
            "ingredients": ["lamb liver", "lamb heart", "steel cut oats", "onions", "suet", "nutmeg", "mace", "black pepper", "thyme", "salt", "natural casing"],
            "instructions": [
                "Boil liver and heart until tender, about 1.5 hours",
                "Cool and mince the cooked organs finely",
                "Toast oats in dry pan until fragrant",
                "Sauté diced onions until soft",
                "Mix minced organs with oats, onions, and suet",
                "Season generously with spices and herbs",
                "Stuff mixture into natural casing and tie ends",
                "Boil wrapped haggis for 3 hours, turning occasionally"
            ],
            "cooking_time": 180,
            "prep_time": 45,
            "difficulty": DifficultyLevel.HARD,
            "servings": 8,
            "budget": 6.50,
            "calories_per_serving": 320,
            "cuisine": "Scottish",
            "dietary_restrictions": DietaryRestriction.NONE,
            "image_url": "https://picsum.photos/400/300?random=41"
        },
        {
            "title": "Belgian Carbonnade",
            "description": "Beer-braised beef stew with caramelized onions",
            "ingredients": ["beef chuck", "belgian dark beer", "onions", "brown sugar", "dijon mustard", "bay leaves", "thyme", "flour", "butter", "bread"],
            "instructions": [
                "Cut beef into large chunks and dust with flour",
                "Brown beef in batches in heavy pot",
                "Slowly cook sliced onions until deeply caramelized",
                "Add brown sugar to onions and caramelize further",
                "Return beef to pot with onions",
                "Add beer, mustard, and herbs",
                "Simmer covered for 2 hours until beef is tender",
                "Serve with crusty bread and mustard"
            ],
            "cooking_time": 150,
            "prep_time": 20,
            "difficulty": DifficultyLevel.MEDIUM,
            "servings": 6,
            "budget": 9.50,
            "calories_per_serving": 420,
            "cuisine": "Belgian",
            "dietary_restrictions": DietaryRestriction.NONE,
            "image_url": "https://picsum.photos/400/300?random=42"
        },
        {
            "title": "Malaysian Rendang",
            "description": "Slow-cooked coconut curry with tender beef",
            "ingredients": ["beef chuck", "coconut milk", "lemongrass", "galangal", "shallots", "garlic", "chilies", "tamarind", "palm sugar", "kerisik", "kaffir lime leaves"],
            "instructions": [
                "Blend shallots, garlic, chilies, galangal into paste",
                "Cut beef into chunks and marinate with salt",
                "Toast grated coconut until golden brown for kerisik",
                "Fry spice paste in oil until fragrant",
                "Add beef and brown on all sides",
                "Add coconut milk and bring to boil",
                "Add lemongrass, lime leaves, tamarind, and palm sugar",
                "Simmer 3-4 hours, stirring occasionally until dry",
                "Stir in kerisik in last 30 minutes"
            ],
            "cooking_time": 240,
            "prep_time": 30,
            "difficulty": DifficultyLevel.HARD,
            "servings": 6,
            "budget": 11.50,
            "calories_per_serving": 480,
            "cuisine": "Malaysian",
            "dietary_restrictions": DietaryRestriction.NONE,
            "image_url": "https://picsum.photos/400/300?random=43"
        },
        {
            "title": "Irish Colcannon",
            "description": "Creamy mashed potatoes with cabbage and scallions",
            "ingredients": ["potatoes", "cabbage", "scallions", "butter", "milk", "salt", "white pepper", "parsley"],
            "instructions": [
                "Boil peeled potatoes until very tender",
                "Shred cabbage finely and cook in salted water until soft",
                "Drain cabbage thoroughly and squeeze out excess water",
                "Mash potatoes with butter and warm milk",
                "Chop scallions finely, including green parts",
                "Fold cooked cabbage and scallions into mashed potatoes",
                "Season with salt and white pepper",
                "Serve hot with a well of melted butter and parsley"
            ],
            "cooking_time": 25,
            "prep_time": 15,
            "difficulty": DifficultyLevel.EASY,
            "servings": 6,
            "budget": 3.00,
            "calories_per_serving": 180,
            "cuisine": "Irish",
            "dietary_restrictions": DietaryRestriction.VEGETARIAN,
            "image_url": "https://picsum.photos/400/300?random=44"
        },
        {
            "title": "Japanese Ramen",
            "description": "Rich pork bone broth with noodles and traditional toppings",
            "ingredients": ["pork bones", "ramen noodles", "pork belly", "soft-boiled eggs", "scallions", "nori", "bamboo shoots", "miso paste", "soy sauce", "garlic", "ginger"],
            "instructions": [
                "Simmer pork bones for 12+ hours to make tonkotsu broth",
                "Char pork belly and braise until tender",
                "Soft-boil eggs and marinate in soy sauce mixture",
                "Prepare toppings: slice scallions, prepare nori and bamboo shoots",
                "Cook fresh ramen noodles according to package instructions",
                "Heat bowls and add miso paste if desired",
                "Ladle hot broth over noodles",
                "Top with sliced pork, halved egg, and other garnishes"
            ],
            "cooking_time": 720,
            "prep_time": 45,
            "difficulty": DifficultyLevel.HARD,
            "servings": 4,
            "budget": 13.00,
            "calories_per_serving": 620,
            "cuisine": "Japanese",
            "dietary_restrictions": DietaryRestriction.NONE,
            "image_url": "https://picsum.photos/400/300?random=45"
        },
        {
            "title": "French Coq au Vin",
            "description": "Chicken braised in red wine with vegetables and herbs",
            "ingredients": ["chicken pieces", "red wine", "bacon", "pearl onions", "mushrooms", "carrots", "tomato paste", "bay leaves", "thyme", "butter", "flour"],
            "instructions": [
                "Marinate chicken pieces in red wine overnight",
                "Remove chicken and strain wine, reserving both",
                "Cook diced bacon until crispy, remove and set aside",
                "Brown chicken pieces in bacon fat",
                "Sauté pearl onions, mushrooms, and carrots",
                "Add tomato paste and cook 2 minutes",
                "Return chicken and add reserved wine and herbs",
                "Braise covered for 45 minutes until tender",
                "Thicken sauce with butter and flour roux"
            ],
            "cooking_time": 75,
            "prep_time": 30,
            "difficulty": DifficultyLevel.MEDIUM,
            "servings": 4,
            "budget": 12.00,
            "calories_per_serving": 520,
            "cuisine": "French",
            "dietary_restrictions": DietaryRestriction.NONE,
            "image_url": "https://picsum.photos/400/300?random=46"
        },
        {
            "title": "Mexican Pozole",
            "description": "Hominy soup with pork and traditional garnishes",
            "ingredients": ["pork shoulder", "hominy", "dried guajillo chiles", "garlic", "onion", "bay leaves", "oregano", "cabbage", "radishes", "lime", "cilantro"],
            "instructions": [
                "Simmer pork shoulder in salted water for 2 hours",
                "Remove pork, shred when cool, strain and reserve broth",
                "Toast and soak dried chiles, blend with garlic",
                "Strain chile mixture and cook in oil until thickened",
                "Add chile sauce to pork broth",
                "Add drained hominy and shredded pork",
                "Simmer 30 minutes to blend flavors",
                "Serve with diced cabbage, radishes, lime, and oregano"
            ],
            "cooking_time": 150,
            "prep_time": 30,
            "difficulty": DifficultyLevel.MEDIUM,
            "servings": 8,
            "budget": 8.50,
            "calories_per_serving": 320,
            "cuisine": "Mexican",
            "dietary_restrictions": DietaryRestriction.NONE,
            "image_url": "https://picsum.photos/400/300?random=47"
        },
        {
            "title": "Indian Biryani",
            "description": "Layered rice dish with spiced meat and aromatics",
            "ingredients": ["basmati rice", "mutton", "yogurt", "onions", "saffron", "mint", "cilantro", "garam masala", "bay leaves", "cinnamon", "cardamom", "cloves", "ghee"],
            "instructions": [
                "Soak basmati rice for 30 minutes, then parboil with whole spices",
                "Marinate mutton with yogurt and spices for 2 hours",
                "Fry sliced onions until golden and crispy",
                "Cook marinated mutton until 70% done",
                "Soak saffron in warm milk",
                "Layer rice and mutton alternately in heavy pot",
                "Top with fried onions, herbs, saffron milk, and ghee",
                "Cook on high heat 5 minutes, then low heat 45 minutes",
                "Rest 10 minutes before opening"
            ],
            "cooking_time": 60,
            "prep_time": 180,
            "difficulty": DifficultyLevel.HARD,
            "servings": 8,
            "budget": 14.00,
            "calories_per_serving": 520,
            "cuisine": "Indian",
            "dietary_restrictions": DietaryRestriction.NONE,
            "image_url": "https://picsum.photos/400/300?random=48"
        },
        {
            "title": "Portuguese Pastéis de Nata",
            "description": "Creamy custard tarts with caramelized tops",
            "ingredients": ["puff pastry", "egg yolks", "sugar", "cornstarch", "milk", "heavy cream", "vanilla", "cinnamon", "lemon zest"],
            "instructions": [
                "Make custard by heating milk and cream with lemon zest",
                "Whisk egg yolks with sugar and cornstarch",
                "Temper egg mixture with hot milk, then return to heat",
                "Cook custard stirring constantly until thick",
                "Strain and cool custard completely",
                "Roll puff pastry and cut into spirals",
                "Press spirals into muffin tins to form cups",
                "Fill with custard and bake at 475°F until tops are spotted",
                "Cool slightly and dust with cinnamon"
            ],
            "cooking_time": 15,
            "prep_time": 45,
            "difficulty": DifficultyLevel.MEDIUM,
            "servings": 12,
            "budget": 5.50,
            "calories_per_serving": 220,
            "cuisine": "Portuguese",
            "dietary_restrictions": DietaryRestriction.VEGETARIAN,
            "image_url": "https://picsum.photos/400/300?random=49"
        },
        {
            "title": "South African Bobotie",
            "description": "Spiced mince baked with egg custard topping",
            "ingredients": ["ground lamb", "onions", "curry powder", "turmeric", "bay leaves", "dried apricots", "almonds", "bread", "milk", "eggs", "chutney", "lemon juice"],
            "instructions": [
                "Soak bread in milk, then squeeze out excess and crumble",
                "Brown ground lamb with onions until cooked",
                "Add curry powder, turmeric, and cook until fragrant",
                "Stir in chopped apricots, almonds, and soaked bread",
                "Add chutney and lemon juice, season well",
                "Press mixture into baking dish with bay leaves on top",
                "Beat eggs with reserved milk for custard",
                "Pour custard over meat mixture",
                "Bake at 350°F for 35 minutes until golden"
            ],
            "cooking_time": 35,
            "prep_time": 20,
            "difficulty": DifficultyLevel.MEDIUM,
            "servings": 6,
            "budget": 8.50,
            "calories_per_serving": 380,
            "cuisine": "South African",
            "dietary_restrictions": DietaryRestriction.NONE,
            "image_url": "https://picsum.photos/400/300?random=50"
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