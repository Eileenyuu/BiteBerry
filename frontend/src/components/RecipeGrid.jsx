import RecipeCard from "./RecipeCard";
import RecommendationStats from "./RecommendationStats";

const RecipeGrid = ({
  recipes,
  recommendationData,
  hasSearched,
  prefs,
  onToggleLike,
  onViewRecipe,
}) => {
  // Show recipes if available
  if (recipes.length > 0) {
    return (
      <div className="space-y-6">
        <div className="text-center">
          <RecommendationStats recommendationData={recommendationData} />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 w-full max-w-none">
          {recipes.map((recipe, index) => (
            <RecipeCard
              key={recipe.recipe_id || index}
              recipe={recipe}
              onToggleLike={onToggleLike}
              onViewRecipe={onViewRecipe}
            />
          ))}
        </div>
      </div>
    );
  }

  // Show empty states
  return (
    <div className="w-full text-center py-12">
      <div
        className={`w-full max-w-5xl mx-auto p-12 rounded-xl ${
          hasSearched
            ? "bg-red-50 border-2 border-red-200"
            : "bg-yellow-50 border-2 border-yellow-200"
        }`}
      >
        {!hasSearched ? (
          <div className="space-y-4 px-8">
            <div className="text-6xl mb-4">🍳</div>
            <h3 className="text-2xl font-bold text-gray-900">
              Ready to discover amazing recipes?
            </h3>
            <p className="text-lg text-gray-600">
              Set your preferences above and click "Find My Perfect Recipes" to
              get personalized recommendations just for you!
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="text-6xl mb-4">😔</div>
            <h3 className="text-xl font-bold text-gray-900">
              No recipes found
            </h3>
            <p className="text-gray-600">
              No recipes match your current preferences. Try increasing your
              budget (currently{" "}
              <span className="font-semibold text-red-600">
                £{prefs.max_budget}
              </span>
              ) or cooking time (currently{" "}
              <span className="font-semibold text-red-600">
                {prefs.max_cooking_time} minutes
              </span>
              ) to see more options!
            </p>
            <div className="pt-2">
              <p className="text-sm text-gray-500">
                💡 Tip: Most recipes are under £10 and take 30-45 minutes
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default RecipeGrid;
