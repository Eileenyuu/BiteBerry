import { useState } from "react";

const NavigationBar = ({ user, onLogout }) => {
  const [isProfileOpen, setIsProfileOpen] = useState(false);

  return (
    <nav className="bg-gradient-to-r from-red-500 to-pink-500 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <h1 className="text-white text-2xl font-bold flex items-center">
                🍓 BiteBerry
              </h1>
            </div>
          </div>

          {/* Navigation Links */}
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-4">
              <a
                href="#preferences"
                className="text-white hover:bg-red-600 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
              >
                🍽️ Preferences
              </a>
              <a
                href="#recipes"
                className="text-red-200 hover:bg-red-600 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
              >
                📖 All Recipes
              </a>
              <a
                href="#favorites"
                className="text-red-200 hover:bg-red-600 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
              >
                ❤️ My Favorites
              </a>
            </div>
          </div>

          {/* User Profile */}
          <div className="relative">
            <button
              onClick={() => setIsProfileOpen(!isProfileOpen)}
              className="flex items-center text-white hover:text-red-200 transition-colors"
            >
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
                  <span className="text-sm font-semibold">
                    {user?.username?.charAt(0)?.toUpperCase()}
                  </span>
                </div>
                <span className="hidden md:block text-sm font-medium">
                  {user?.username}
                </span>
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
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
      </div>

      {/* Mobile menu */}
      <div className="md:hidden">
        <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-red-600">
          <a
            href="#preferences"
            className="text-white block px-3 py-2 text-base font-medium"
          >
            🍽️ Preferences
          </a>
          <a
            href="#recipes"
            className="text-red-200 hover:text-white block px-3 py-2 text-base font-medium"
          >
            📖 All Recipes
          </a>
          <a
            href="#favorites"
            className="text-red-200 hover:text-white block px-3 py-2 text-base font-medium"
          >
            ❤️ My Favorites
          </a>
        </div>
      </div>
    </nav>
  );
};

export default NavigationBar;