import { useState } from "react";
import { getRecommendations } from "../api/recipes";
import { likeRecipe, unlikeRecipe } from "../api/likes";

export const useRecipes = (user) => {
  const [recipes, setRecipes] = useState([]);
  const [recommendationData, setRecommendationData] = useState(null);
  const [hasSearched, setHasSearched] = useState(false);
  const [loading, setLoading] = useState(false);

  // Fetch recipe recommendations
  const fetchRecommendations = async (preferences) => {
    if (!user?.id || !preferences) return;

    setLoading(true);
    try {
      const response = await getRecommendations(user.id, preferences);
      setRecipes(response.recommendations || []);
      setRecommendationData(response);
      setHasSearched(true);

      // Log AI recommendation info for debugging
      console.log("🔍 Recommendation response:", {
        total: response.total_count,
        ai_count: response.ai_count,
        has_ai: response.has_ai_recommendations,
        recipes_with_ai_type:
          response.recommendations?.filter(
            (r) => r.recommendation_type === "ai"
          ).length || 0,
      });

      if (response.has_ai_recommendations) {
        console.log(
          `✨ Found ${response.ai_count} AI recommendations out of ${response.total_count} total`
        );
      } else {
        console.log("❌ No AI recommendations found");
      }
    } catch (error) {
      console.error("Failed to fetch recommendations:", error);
    } finally {
      setLoading(false);
    }
  };

  // Toggle like/unlike recipe
  const handleToggleLike = async (recipeId) => {
    if (!user?.id) return;

    const recipe = recipes.find((r) => r.id === recipeId);
    if (!recipe) return;

    try {
      if (recipe.user_has_liked) {
        // Unlike the recipe
        await unlikeRecipe(recipeId, user.id);

        // Update state to reflect unlike
        setRecipes((prevRecipes) =>
          prevRecipes.map((r) => {
            if (r.id === recipeId) {
              return {
                ...r,
                like_count: Math.max(0, r.like_count - 1),
                user_has_liked: false,
              };
            }
            return r;
          })
        );
      } else {
        // Like the recipe
        await likeRecipe(recipeId, user.id);

        // Update state to reflect like
        setRecipes((prevRecipes) =>
          prevRecipes.map((r) => {
            if (r.id === recipeId) {
              return {
                ...r,
                like_count: r.like_count + 1,
                user_has_liked: true,
              };
            }
            return r;
          })
        );
      }
    } catch (error) {
      console.error("Failed to toggle like:", error);
    }
  };

  return {
    recipes,
    recommendationData,
    hasSearched,
    loading,
    fetchRecommendations,
    handleToggleLike,
  };
};
