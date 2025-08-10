const RecipeCard = ({ recipe, onToggleLike, onViewRecipe }) => {
  return (
    <div className="w-full bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 overflow-hidden group">
      {/* Recipe Image Placeholder */}
      <div className="h-48 bg-gradient-to-br from-red-400 to-pink-400 flex items-center justify-center">
        <span className="text-6xl opacity-80">🍽️</span>
      </div>

      {/* Recipe Content */}
      <div className="p-6">
        <div className="flex items-start justify-between mb-3">
          <h3 className="text-xl font-bold text-gray-900 group-hover:text-red-600 transition-colors">
            {recipe.title}
          </h3>
          <div className="flex gap-2">
            {recipe.recommendation_type === "ai" && (
              <span className="bg-gradient-to-r from-purple-500 to-pink-500 text-white text-xs font-bold px-2 py-1 rounded-full shadow-sm">
                🤖 AI Suggested
              </span>
            )}
            {recipe.recommendation_type === "popular" && (
              <span className="bg-gradient-to-r from-orange-500 to-red-500 text-white text-xs font-bold px-2 py-1 rounded-full shadow-sm">
                🔥 Popular
              </span>
            )}
            {recipe.cuisine && (
              <span className="bg-red-100 text-red-800 text-xs font-medium px-2 py-1 rounded-full">
                {recipe.cuisine}
              </span>
            )}
          </div>
        </div>

        <p className="text-gray-600 text-sm mb-4 line-clamp-2">
          {recipe.description}
        </p>

        {/* Recipe Stats */}
        <div className="flex items-center gap-4 mb-4 text-sm text-gray-500">
          <div className="flex items-center">
            <span className="text-green-500 mr-1">💰</span>£{recipe.budget}
          </div>
          <div className="flex items-center">
            <span className="text-orange-500 mr-1">⏰</span>
            {recipe.cooking_time}min
          </div>
          <div className="flex items-center">
            <span className="text-purple-500 mr-1">👥</span>
            {recipe.servings} serving{recipe.servings > 1 ? "s" : ""}
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center justify-between">
          <button
            onClick={() => onToggleLike(recipe.id)}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
              recipe.user_has_liked
                ? "bg-red-100 text-red-700 hover:bg-red-200"
                : "bg-gray-100 text-gray-700 hover:bg-red-100 hover:text-red-700"
            }`}
          >
            <span
              className={`transition-all duration-200 ${
                recipe.user_has_liked ? "text-red-500 scale-110" : ""
              }`}
            >
              {recipe.user_has_liked ? "❤️" : "🤍"}
            </span>
            <span className="text-sm">{recipe.like_count || 0}</span>
          </button>

          <button
            onClick={() => onViewRecipe(recipe.id)}
            className="bg-gradient-to-r from-blue-500 to-blue-600 text-white px-4 py-2 rounded-lg hover:from-blue-600 hover:to-blue-700 transition-all duration-200 font-medium shadow-md hover:shadow-lg"
          >
            View Recipe →
          </button>
        </div>
      </div>
    </div>
  );
};

export default RecipeCard;