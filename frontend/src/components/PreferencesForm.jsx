import { getDietaryRestrictionOptions, DIETARY_RESTRICTIONS } from "../constants/enums";

const PreferencesForm = ({ 
  prefs, 
  status, 
  loading, 
  onInputChange, 
  onSubmit 
}) => {
  return (
    <div className="w-full bg-white rounded-xl shadow-lg p-8 mb-8">
      <form onSubmit={onSubmit} className="space-y-6">
        {/* Grid Layout for Form Fields */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Budget Input */}
          <div className="space-y-2">
            <label
              htmlFor="max_budget"
              className="text-sm font-semibold text-gray-700 flex items-center"
            >
              💰 Maximum Budget
            </label>
            <div className="relative">
              <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 font-medium">
                £
              </span>
              <input
                type="number"
                id="max_budget"
                name="max_budget"
                value={prefs.max_budget}
                onChange={onInputChange}
                min="1"
                max="100"
                step="0.01"
                placeholder="15.00"
                className="pl-8 w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500 transition-colors"
              />
            </div>
            <p className="text-xs text-gray-500">
              How much would you like to spend per meal?
            </p>
          </div>

          {/* Cooking Time Input */}
          <div className="space-y-2">
            <label
              htmlFor="max_cooking_time"
              className="text-sm font-semibold text-gray-700 flex items-center"
            >
              ⏰ Maximum Cooking Time
            </label>
            <div className="relative">
              <input
                type="number"
                id="max_cooking_time"
                name="max_cooking_time"
                value={prefs.max_cooking_time}
                onChange={onInputChange}
                min="10"
                max="180"
                placeholder="30"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500 transition-colors"
              />
              <span className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 font-medium">
                mins
              </span>
            </div>
            <p className="text-xs text-gray-500">
              How long are you willing to cook?
            </p>
          </div>
        </div>

        {/* Dietary Restrictions */}
        <div className="space-y-2">
          <label
            htmlFor="dietary_restrictions"
            className="text-sm font-semibold text-gray-700 flex items-center"
          >
            🥗 Dietary Preferences
          </label>
          <select
            id="dietary_restrictions"
            name="dietary_restrictions"
            value={prefs.dietary_restrictions || DIETARY_RESTRICTIONS.NONE}
            onChange={onInputChange}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500 transition-colors bg-white"
          >
            {getDietaryRestrictionOptions().map((option) => (
              <option key={option.value} value={option.value}>
                {option.emoji} {option.label}
              </option>
            ))}
          </select>
          <p className="text-xs text-gray-500">
            Any special dietary requirements?
          </p>
        </div>

        {/* Submit Button */}
        <div className="pt-4">
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-gradient-to-r from-red-500 to-pink-500 text-white font-semibold py-4 px-6 rounded-lg hover:from-red-600 hover:to-pink-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-lg hover:shadow-xl"
          >
            {loading ? (
              <span className="flex items-center justify-center">
                <svg
                  className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  ></circle>
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
                Finding Perfect Recipes...
              </span>
            ) : (
              "🔍 Find My Perfect Recipes"
            )}
          </button>
        </div>

        {/* Status Message */}
        {status && (
          <div
            className={`mt-4 p-4 rounded-lg border ${
              status.includes("successfully")
                ? "bg-green-50 border-green-200 text-green-800"
                : "bg-red-50 border-red-200 text-red-800"
            }`}
          >
            <div className="flex items-center justify-center">
              <span className="mr-2">
                {status.includes("successfully") ? "✅" : "❌"}
              </span>
              {status}
            </div>
          </div>
        )}
      </form>
    </div>
  );
};

export default PreferencesForm;