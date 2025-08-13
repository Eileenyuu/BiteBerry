import WeeklyCalendar from "../components/WeeklyCalendar";

const MealPlanning = ({ user, onNavigate }) => {
  return (
    <div className="min-h-screen w-full">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            📅 Meal Planning
          </h1>
          <p className="text-lg text-gray-600">
            Plan your meals for the week ahead
          </p>
        </div>

        {/* Weekly Calendar */}
        <WeeklyCalendar user={user} onNavigate={onNavigate} />

        {/* Tips Section */}
        <div className="mt-8 bg-blue-50 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-3">
            💡 Meal Planning Tips
          </h3>
          <ul className="text-blue-800 space-y-1">
            <li>• Click empty slots to add meals from your liked recipes</li>
            <li>• Click existing meals to remove them</li>
            <li>• Use the arrows to navigate between weeks</li>
            <li>• Generate shopping lists from your meal plans</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default MealPlanning;
