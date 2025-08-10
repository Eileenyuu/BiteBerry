import { useState } from "react";

const NavigationBar = ({ user, onLogout, currentPage, onNavigate }) => {
  const [isProfileOpen, setIsProfileOpen] = useState(false);

  return (
    <nav className="bg-gradient-to-r from-red-400 to-pink-600 shadow-lg px-4 md:px-6 lg:px-8 py-4 z-50">
      <div className="flex items-center justify-between">
        {/* Logo */}
        <div className="flex-shrink-0">
          <h1 className="text-white text-2xl font-bold flex items-center">
            🍓 BiteBerry
          </h1>
        </div>

        {/* Navigation Links - Center */}
        <div className="hidden md:flex items-center space-x-4">
          <button
            onClick={() => onNavigate("preferences")}
            className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
              currentPage === "preferences"
                ? "bg-red-600 text-white"
                : "text-red-200 hover:bg-red-600 hover:text-white"
            }`}
          >
            🍽️ Preferences
          </button>

          <button
            onClick={() => onNavigate("recipes_all")}
            className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
              currentPage === "recipes_all"
                ? "bg-red-600 text-white"
                : "text-red-200 hover:bg-red-600 hover:text-white"
            }`}
          >
            📖 All Recipes
          </button>
        </div>

        {/* User Profile - Right */}
        <div className="relative flex-shrink-0">
          <button
            onClick={() => setIsProfileOpen(!isProfileOpen)}
            className="flex items-center border-2 border-pink-300 text-white hover:bg-red-500 transition-colors px-2 py-1 rounded-lg"
          >
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-r from-pink-300 to-red-400 rounded-full flex items-center justify-center border-2 border-white border-opacity-70">
                <span className="text-sm font-semibold text-white">
                  {user?.username?.charAt(0)?.toUpperCase()}
                </span>
              </div>
              <span className="hidden sm:block text-sm font-medium">
                {user?.username}
              </span>
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                  clipRule="evenodd"
                />
              </svg>
            </div>
          </button>

          {/* Dropdown */}
          {isProfileOpen && (
            <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-50">
              <div className="px-4 py-2 text-sm text-gray-700 border-b">
                <div className="font-medium">{user?.username}</div>
                <div className="text-xs text-gray-500">{user?.email}</div>
              </div>
              <a
                href="#profile"
                className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              >
                👤 Profile Settings
              </a>
              <a
                href="#help"
                className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              >
                ❓ Help & Support
              </a>
              <button
                onClick={onLogout}
                className="block w-full text-left px-4 py-2 text-sm text-red-700 hover:bg-red-50"
              >
                🚪 Sign Out
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Mobile Navigation */}
      <div className="md:hidden mt-4 pb-2">
        <div className="flex flex-col space-y-2">
          <button
            onClick={() => onNavigate("preferences")}
            className={`px-3 py-2 rounded-md text-sm font-medium transition-colors text-left ${
              currentPage === "preferences"
                ? "bg-red-600 text-white"
                : "text-red-200 hover:bg-red-600 hover:text-white"
            }`}
          >
            🍽️ Preferences
          </button>
          <button
            onClick={() => onNavigate("recipes_all")}
            className={`px-3 py-2 rounded-md text-sm font-medium transition-colors text-left ${
              currentPage === "recipes_all"
                ? "bg-red-600 text-white"
                : "text-red-200 hover:bg-red-600 hover:text-white"
            }`}
          >
            📖 All Recipes
          </button>
        </div>
      </div>
    </nav>
  );
};

export default NavigationBar;
