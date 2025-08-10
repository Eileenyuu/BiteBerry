// 1. Import dependency
import { useState } from "react";
import { useAllRecipes } from "../hooks/useAllRecipes";
import RecipeGrid from "../components/RecipeGrid";
import RecipeDetail from "./recipes_detail";

// 2. Hook and state
const RecipesAll = ({ user }) => {
  const { recipes, loading, error, handleToggleLike } = useAllRecipes(user);
  const [selectedRecipeId, setSelectedRecipeId] = useState(null);
  const [showDetail, setShowDetail] = useState(false);

  // 3. Navigation handlers
  const handleViewRecipe = (recipeId) => {
    setSelectedRecipeId(recipeId);
    setShowDetail(true);
  };

  const handleBackToList = () => {
    setSelectedRecipeId(null);
    setShowDetail(false);
  };

  // 4. Show recipe detail if selected
  if (showDetail && selectedRecipeId !== null) {
    return (
      <div className="recipes-container">
        <RecipeDetail recipeId={selectedRecipeId} onBack={handleBackToList} />
      </div>
    );
  }

  // 5. Loading state
  if (loading) {
    return (
      <div className="text-center py-12 text-lg">Loading all recipes...</div>
    );
  }

  // 6. Error state
  if (error) {
    return <div className="text-center py-12 text-red-600">{error}</div>;
  }

  // 7. Main recipes view
  return (
    <div className="min-h-screen w-full">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">All Recipes</h1>
          <p className="text-lg text-gray-600">
            Discover our complete collection of delicious recipes!
          </p>
        </div>

        {/* Use existing RecipeGrid component */}
        <div className="w-full overflow-hidden">
          <RecipeGrid
            recipes={recipes}
            recommendationData={null} // No AI recommendations here
            hasSearched={true} // Always show "no recipes" if empty
            prefs={{ max_budget: "∞", max_cooking_time: "∞" }} // For empty state
            onToggleLike={handleToggleLike}
            onViewRecipe={handleViewRecipe}
          />
        </div>
      </div>
    </div>
  );
};

export default RecipesAll;
