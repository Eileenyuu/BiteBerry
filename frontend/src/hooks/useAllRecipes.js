import { useState, useEffect } from "react";
import { getAllRecipes } from "../api/recipes";
import { likeRecipe, unlikeRecipe } from "../api/likes";

export const useAllRecipes = (user) => {
  // States: recipes, loading, error
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Functions: fetchAllRecipes
  const fetchAllRecipes = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await getAllRecipes(user?.id);
      setRecipes(response);
    } catch (error) {
      setError("Failed to fetch recipes");
      console.error("Error fetching all recipes: ", error);
    } finally {
      setLoading(false);
    }
  };

  // Effects: fetch recipes on mount and when user changes
  useEffect(() => {
    fetchAllRecipes();
  }, [user?.id]); //Refetch when user ID changes

  // Function: handleToggleLike
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

        // Update the like
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
      console.error("Failed to toggle like", error);
    }
  };

  return {
    recipes,
    loading,
    error,
    handleToggleLike,
  };
};
