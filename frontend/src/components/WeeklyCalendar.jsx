import { useState, useEffect } from "react";
import {
  getWeeklyMealPlan,
  addMealPlan,
  deleteMealPlan,
} from "../api/meal_planning";
import { getUserLikedRecipes } from "../api/likes";
import { createShoppingListFromMealPlans } from "../api/shopping";

const WeeklyCalendar = ({ user, onNavigate }) => {
  const [currentWeekStart, setCurrentWeekStart] = useState(
    getMonday(new Date())
  );
  const [mealPlans, setMealPlans] = useState([]);
  const [recipes, setRecipes] = useState([]);
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedSlot, setSelectedSlot] = useState({
    date: null,
    mealType: null,
  });
  const [loading, setLoading] = useState(false);
  const [showSuccessModal, setShowSuccessModal] = useState(false);

  const mealTypes = ["breakfast", "lunch", "dinner"];
  const weekDays = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
  ];

  useEffect(() => {
    if (user?.id) {
      fetchWeeklyPlan();
      fetchRecipes();
    }
  }, [user, currentWeekStart]);

  function getMonday(date) {
    const d = new Date(date);
    const day = d.getDay();
    const diff = d.getDate() - day + (day === 0 ? -6 : 1); // Adjust when day is Sunday
    return new Date(d.setDate(diff));
  }

  const fetchWeeklyPlan = async () => {
    try {
      const weekStart = currentWeekStart.toISOString().split("T")[0];
      const weeklyData = await getWeeklyMealPlan(user.id, weekStart);
      setMealPlans(weeklyData.meal_plans || []);
    } catch (error) {
      console.error("Error fetching weekly meal plan:", error);
    }
  };

  const fetchRecipes = async () => {
    try {
      const likedRecipes = await getUserLikedRecipes(user.id);
      setRecipes(likedRecipes);
    } catch (error) {
      console.error("Error fetching recipes:", error);
    }
  };

  const navigateWeek = (direction) => {
    const newDate = new Date(currentWeekStart);
    newDate.setDate(newDate.getDate() + direction * 7);
    setCurrentWeekStart(newDate);
  };

  const getDateForDay = (dayIndex) => {
    const date = new Date(currentWeekStart);
    date.setDate(date.getDate() + dayIndex);
    return date;
  };

  const getMealForSlot = (date, mealType) => {
    return mealPlans.find((plan) => {
      const planDate = new Date(plan.meal_date).toDateString();
      const slotDate = date.toDateString();
      return planDate === slotDate && plan.meal_type === mealType;
    });
  };

  const handleSlotClick = (date, mealType) => {
    const existingMeal = getMealForSlot(date, mealType);
    if (existingMeal) {
      // Delete existing meal
      handleDeleteMeal(existingMeal.id);
    } else {
      // Add new meal
      setSelectedSlot({ date, mealType });
      setShowAddModal(true);
    }
  };

  const handleAddMeal = async (recipeId) => {
    setLoading(true);
    try {
      // Create date at noon to avoid timezone issues
      const mealDate = new Date(selectedSlot.date);
      mealDate.setHours(12, 0, 0, 0); // Set to noon

      const mealPlanData = {
        recipe_id: recipeId,
        meal_date: mealDate.toISOString(),
        meal_type: selectedSlot.mealType,
        servings: 2,
      };

      await addMealPlan(user.id, mealPlanData);
      await fetchWeeklyPlan(); // Refresh the calendar
      setShowAddModal(false);
    } catch (error) {
      console.error("Error adding meal:", error);
      alert("Failed to add meal");
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteMeal = async (mealPlanId) => {
    try {
      await deleteMealPlan(mealPlanId, user.id);
      await fetchWeeklyPlan(); // Refresh the calendar
    } catch (error) {
      console.error("Error deleting meal:", error);
      alert("Failed to delete meal");
    }
  };

  const getRecipeTitle = (recipeId) => {
    const recipe = recipes.find((r) => r.id === recipeId);
    return recipe ? recipe.title : "Unknown Recipe";
  };

  const handleGenerateShoppingList = async () => {
    if (mealPlans.length === 0) {
      alert("No meal plans found for this week!");
      return;
    }

    setLoading(true);
    try {
      const startDate = currentWeekStart.toISOString().split("T")[0];
      const endDate = getDateForDay(6).toISOString().split("T")[0];

      await createShoppingListFromMealPlans(user.id, startDate, endDate);
      setShowSuccessModal(true);
    } catch (error) {
      console.error("Error creating shopping list:", error);
      alert("Failed to create shopping list");
    } finally {
      setLoading(false);
    }
  };

  const handleViewShoppingList = () => {
    setShowSuccessModal(false);
    if (onNavigate) {
      onNavigate("shopping");
    }
  };

  const handleStayHere = () => {
    setShowSuccessModal(false);
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Weekly Meal Plan</h2>
        <div className="flex items-center space-x-4">
          <button
            onClick={() => navigateWeek(-1)}
            className="p-2 hover:bg-gray-100 rounded-lg"
          >
            ← Previous
          </button>
          <span className="font-medium text-lg">
            {currentWeekStart.toDateString()} -{" "}
            {getDateForDay(6).toDateString()}
          </span>
          <button
            onClick={() => navigateWeek(1)}
            className="p-2 hover:bg-gray-100 rounded-lg"
          >
            Next →
          </button>
        </div>
      </div>

      {/* Calendar Grid */}
      <div className="grid grid-cols-8 gap-2">
        {/* Header Row */}
        <div className="font-medium text-center text-gray-600"></div>
        {weekDays.map((day, index) => (
          <div key={day} className="font-medium text-center text-gray-600 py-2">
            <div>{day}</div>
            <div className="text-sm text-gray-400">
              {getDateForDay(index).getDate()}
            </div>
          </div>
        ))}

        {/* Meal Rows */}
        {mealTypes.map((mealType) => (
          <>
            <div
              key={mealType}
              className="font-medium text-gray-600 py-4 capitalize"
            >
              {mealType}
            </div>
            {weekDays.map((_, dayIndex) => {
              const date = getDateForDay(dayIndex);
              const meal = getMealForSlot(date, mealType);

              return (
                <div
                  key={`${mealType}-${dayIndex}`}
                  onClick={() => handleSlotClick(date, mealType)}
                  className={`min-h-20 border border-gray-200 rounded-lg p-2 cursor-pointer transition-colors ${
                    meal ? "bg-red-50 hover:bg-red-100" : "hover:bg-gray-50"
                  }`}
                >
                  {meal ? (
                    <div className="text-sm">
                      <div className="font-medium text-gray-900">
                        {getRecipeTitle(meal.recipe_id)}
                      </div>
                      <div className="text-gray-500 text-xs">
                        {meal.servings} servings
                      </div>
                    </div>
                  ) : (
                    <div className="text-gray-400 text-sm text-center">
                      + Add meal
                    </div>
                  )}
                </div>
              );
            })}
          </>
        ))}
        <div className="col-span-8 flex justify-center mt-4">
          <button
            onClick={handleGenerateShoppingList}
            disabled={loading || mealPlans.length === 0}
            className="px-4 py-2 bg-transparent text-green-600 border border-green-600 rounded-lg hover:bg-green-600 hover:text-white disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Generate Shopping List
          </button>
        </div>
      </div>

      {/* Add Meal Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Add Meal for {selectedSlot.mealType} on{" "}
              {selectedSlot.date?.toDateString()}
            </h3>

            <div className="max-h-60 overflow-y-auto space-y-2">
              {recipes.length === 0 ? (
                <p className="text-gray-500 text-center py-4">
                  No liked recipes found. Like some recipes first!
                </p>
              ) : (
                recipes.map((recipe) => (
                  <button
                    key={recipe.id}
                    onClick={() => handleAddMeal(recipe.id)}
                    disabled={loading}
                    className="w-full text-left p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50"
                  >
                    <div className="font-medium">{recipe.title}</div>
                    <div className="text-sm text-gray-500">
                      {recipe.cooking_time} min • £{recipe.budget}
                    </div>
                  </button>
                ))
              )}
            </div>

            <div className="flex justify-end space-x-3 mt-6">
              <button
                onClick={() => setShowAddModal(false)}
                className="px-4 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Success Modal */}
      {showSuccessModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <div className="text-center">
              <div className="text-xl mb-4">✅</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Shopping List Created!
              </h3>
              <p className="text-gray-600 mb-6">
                Your weekly shopping list has been generated from your meal
                plans.
              </p>

              <div className="flex space-x-3">
                <button
                  onClick={handleViewShoppingList}
                  className="flex-1 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                >
                  View Shopping List
                </button>
                <button
                  onClick={handleStayHere}
                  className="flex-1 px-4 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Stay Here
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default WeeklyCalendar;
