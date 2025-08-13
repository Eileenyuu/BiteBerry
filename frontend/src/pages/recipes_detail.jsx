import { useState, useEffect } from "react";
import { getRecipeDetail } from "../api/recipes";

const RecipeDetail = ({ recipeId, onBack }) => {
  const [recipe, setRecipe] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch Recipe Detail
    const fetchRecipeDetail = async () => {
      try {
        console.log("Fetching recipe detail for ID:", recipeId);
        const recipeDetail = await getRecipeDetail(recipeId);
        console.log("Recipe detail response:", recipeDetail);
        setRecipe(recipeDetail);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching recipe detail:", error);
        console.error("Error details:", error.response?.data);
        setLoading(false);
      }
    };

    if (recipeId) {
      fetchRecipeDetail();
    }
  }, [recipeId]); //Have dependency - first load + execute when dependency changing

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!recipe) {
    return <div>Recipe not found</div>;
  }

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      {/* Header */}
      <div className="mb-6">
        <button
          onClick={onBack}
          className="mb-4 px-6 py-3 bg-transparent border border-red-600 text-red-500 font-semibold rounded-lg hover:bg-red-400 hover:text-white transition-colors shadow-md"
        >
          ← Back to Recipes
        </button>

        <h1 className="text-3xl font-bold text-gray-800 mb-2">
          {recipe.title}
        </h1>
        <p className="text-lg text-gray-600 mb-4">{recipe.description}</p>

        {recipe.cuisine && (
          <span className="inline-block px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
            {recipe.cuisine} Cuisine
          </span>
        )}
      </div>

      {/* Recipe Info Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div className="text-center p-4 bg-green-50 rounded-lg border border-green-200">
          <div className="text-2xl font-bold text-green-700">
            £{recipe.budget}
          </div>
          <div className="text-sm text-green-600">Budget</div>
        </div>
        <div className="text-center p-4 bg-orange-50 rounded-lg border border-orange-200">
          <div className="text-2xl font-bold text-orange-700">
            {recipe.cooking_time} min
          </div>
          <div className="text-sm text-orange-600">Cooking Time</div>
        </div>
        <div className="text-center p-4 bg-purple-50 rounded-lg border border-purple-200">
          <div className="text-2xl font-bold text-purple-700">
            {recipe.servings}
          </div>
          <div className="text-sm text-purple-600">Servings</div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Ingredients */}
        <div className="bg-gray-50 p-6 rounded-lg">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4 flex items-center">
            🥘 Ingredients
          </h2>
          <ul className="space-y-2">
            {recipe.ingredients &&
              recipe.ingredients.map((ingredient, index) => (
                <li key={index} className="flex items-center text-gray-700">
                  <span className="w-2 h-2 bg-red-500 rounded-full mr-3 flex-shrink-0"></span>
                  {ingredient}
                </li>
              ))}
          </ul>
        </div>

        {/* Instructions */}
        <div className="bg-gray-50 p-6 rounded-lg">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4 flex items-center">
            📝 Instructions
          </h2>
          <ol className="space-y-3 text-left">
            {recipe.instructions &&
              recipe.instructions.map((step, index) => (
                <li key={index} className="flex text-gray-700">
                  <span className="bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold mr-3 flex-shrink-0 mt-0.5">
                    {index + 1}
                  </span>
                  <span className="leading-relaxed">{step}</span>
                </li>
              ))}
          </ol>
        </div>
      </div>
    </div>
  );
};

export default RecipeDetail;
