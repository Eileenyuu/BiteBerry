"""
Simple AI-powered recipe recommendation service using SentenceTransformers
"""
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session
from core.models import Recipe, Like
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json
import logging

logger = logging.getLogger(__name__)

class AIRecommendationService:
    def __init__(self):
        self.model = None
    
    def _get_model(self):
        """Lazy load the SentenceTransformer model"""
        if self.model is None:
            logger.info("Loading SentenceTransformer model...")
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
        return self.model
    
    def _recipe_to_text(self, recipe: Recipe) -> str:
        """Convert recipe to text for embedding generation"""
        try:
            ingredients = json.loads(recipe.ingredients) if recipe.ingredients else []
            ingredients_text = " ".join(ingredients[:5])  # First 5 ingredients only
        except (json.JSONDecodeError, TypeError):
            ingredients_text = ""
        
        text_parts = [
            recipe.title,
            recipe.description,
            recipe.cuisine or "",
            ingredients_text
        ]
        
        return " ".join(filter(None, text_parts))
    
    def get_ai_recommendations(self, db: Session, user_id: int, limit: int = 5) -> list:
        """
        Get AI-powered recommendations based on user's liked recipes
        
        Args:
            db: Database session
            user_id: User ID to get recommendations for
            limit: Maximum number of recommendations to return
            
        Returns:
            List of recommended recipe IDs with similarity scores
        """
        try:
            # Get user's liked recipes
            liked_recipe_ids = db.query(Like.recipe_id).filter(Like.user_id == user_id).all()
            liked_recipe_ids = [id[0] for id in liked_recipe_ids]
            
            if not liked_recipe_ids:
                logger.info(f"No liked recipes found for user {user_id}, using popular recipes")
                return self._get_popular_recipes_for_new_users(db, limit)
            
            # Get all recipes
            all_recipes = db.query(Recipe).all()
            if not all_recipes:
                return []
            
            # Get liked recipes
            liked_recipes = [r for r in all_recipes if r.id in liked_recipe_ids]
            if not liked_recipes:
                return []
            
            # Get candidate recipes (not liked by user)
            candidate_recipes = [r for r in all_recipes if r.id not in liked_recipe_ids]
            if not candidate_recipes:
                return []
            
            # Generate embeddings
            model = self._get_model()
            
            # Convert recipes to text
            liked_texts = [self._recipe_to_text(recipe) for recipe in liked_recipes]
            candidate_texts = [self._recipe_to_text(recipe) for recipe in candidate_recipes]
            
            # Generate embeddings
            liked_embeddings = model.encode(liked_texts)
            candidate_embeddings = model.encode(candidate_texts)
            
            # Calculate average liked recipe embedding (user preference profile)
            user_profile = np.mean(liked_embeddings, axis=0).reshape(1, -1)
            
            # Calculate similarity scores
            similarities = cosine_similarity(user_profile, candidate_embeddings)[0]
            
            # Create recommendations with scores
            recommendations = []
            for i, recipe in enumerate(candidate_recipes):
                recommendations.append({
                    'recipe_id': recipe.id,
                    'similarity_score': float(similarities[i]),
                    'recipe': recipe
                })
            
            # Sort by similarity score and return top results
            recommendations.sort(key=lambda x: x['similarity_score'], reverse=True)
            return recommendations[:limit]
            
        except Exception as e:
            logger.error(f"Error generating AI recommendations: {e}")
            return []
    
    def _get_popular_recipes_for_new_users(self, db: Session, limit: int = 5) -> list:
        """
        Get popular recipes for new users who haven't liked anything yet
        
        Args:
            db: Database session
            limit: Maximum number of recommendations to return
            
        Returns:
            List of popular recipes formatted as recommendations
        """
        try:
            # Get recipes ordered by like count (most popular first)
            from sqlalchemy import func
            
            popular_recipes = (
                db.query(Recipe, func.count(Like.id).label('like_count'))
                .outerjoin(Like, Recipe.id == Like.recipe_id)
                .group_by(Recipe.id)
                .order_by(func.count(Like.id).desc(), Recipe.id.asc())
                .limit(limit)
                .all()
            )

            if not popular_recipes:
                return []
            
            like_counts = [like_count for _, like_count in popular_recipes]
            max_like = max(like_counts)
            min_like = min(like_counts)

            max_score = 0.95
            min_score = 0.60
            
            
            recommendations = []
            # for i, (recipe, like_count) in enumerate(popular_recipes):
            #     # Give high scores to maintain ranking
            #     similarity_score = 0.9 - (i * 0.05)
            #     recommendations.append({
            #         'recipe_id': recipe.id,
            #         'similarity_score': max(similarity_score, 0.6),
            #         'recipe': recipe,
            #         'recommendation_type': 'popular',
            #         'like_count': like_count
            #     })

            for recipe, like_count in popular_recipes:
                if max_like == min_like:
                    similarity_score = (max_score + min_score) / 2
                else:
                    similarity_score = min_score + (like_count - min_like) * (max_score - min_score) / (max_like - min_like)
                
                recommendations.append({
                        'recipe_id': recipe.id,
                        'similarity_score': round(similarity_score, 3),
                        'recipe': recipe,
                        'recommendation_type': 'popular',
                        'like_count': like_count
                    })
            
            logger.info(f"Generated {len(recommendations)} popular recipes for new user")
            return recommendations
            
        except Exception as e:
            logger.error(f"Error getting popular recipes: {e}")
            return []

# Global instance
ai_service = AIRecommendationService()