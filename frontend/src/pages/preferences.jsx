import { useState } from "react";
import { usePreferences } from "../hooks/usePreferences";
import { useRecipes } from "../hooks/useRecipes";
import PreferencesForm from "../components/PreferencesForm";
import RecipeGrid from "../components/RecipeGrid";
import RecipeDetail from "./recipes_detail";

const Preferences = ({ user }) => {
  const {
    prefs,
    status,
    loading: prefsLoading,
    handleInputChange,
    savePreferences,
  } = usePreferences(user);
  const {
    recipes,
    recommendationData,
    hasSearched,
    loading: recipesLoading,
    fetchRecommendations,
    handleToggleLike,
  } = useRecipes(user);
  const [selectedRecipeId, setSelectedRecipeId] = useState(null);
  const [showDetail, setShowDetail] = useState(false);

  // Handle form submit
  const handleSubmitPrefs = async (e) => {
    e.preventDefault();
    const parsedPrefs = await savePreferences();
    if (parsedPrefs) {
      await fetchRecommendations(parsedPrefs);
    }
  };

  // Handle View Recipe Detail
  const handleViewRecipe = (recipeId) => {
    setSelectedRecipeId(recipeId);
    setShowDetail(true);
  };

  const handleBackToList = () => {
    setShowDetail(false);
    setSelectedRecipeId(null);
  };

  if (showDetail && selectedRecipeId) {
    return (
      <div className="preferences-container">
        <RecipeDetail recipeId={selectedRecipeId} onBack={handleBackToList} />
      </div>
    );
  }

  return (
    <div className="min-h-screen w-full">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            🍽️ Your Food Preferences
          </h1>
          <p className="text-lg text-gray-600">
            Tell us what you love, and we'll find the perfect recipes for you!
          </p>
        </div>

        {/* Preferences Form */}
        <PreferencesForm
          prefs={prefs}
          status={status}
          loading={prefsLoading || recipesLoading}
          onInputChange={handleInputChange}
          onSubmit={handleSubmitPrefs}
        />

        {/* Recipe Recommendations */}
        <div className="w-full overflow-hidden min-h-96">
          {recipes.length > 0 && (
            <div className="text-center mb-6">
              <h2 className="text-3xl font-bold text-gray-900 mb-2">
                🍽️ Perfect Recipes For You
              </h2>
              <p className="text-gray-600">
                Found {recipes.length} delicious recipes matching your preferences!
              </p>
            </div>
          )}
          <RecipeGrid
            recipes={recipes}
            recommendationData={recommendationData}
            hasSearched={hasSearched}
            prefs={prefs}
            onToggleLike={handleToggleLike}
            onViewRecipe={handleViewRecipe}
          />
        </div>
      </div>
    </div>
  );
};

export default Preferences;
