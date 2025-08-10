import { useState, useEffect } from "react";
import Login from "../pages/login";
import Register from "../pages/register";
import Preferences from "../pages/preferences";
import RecipesAll from "../pages/recipes_all";
import NavigationBar from "./NavigationBar";

const AuthWrapper = () => {
  const [user, setUser] = useState(null);
  const [showRegister, setShowRegister] = useState(false);
  const [currentPage, setCurrentPage] = useState("preferences"); // preferences, shopping, recipes

  useEffect(() => {
    // Check if user is already logged in
    const savedUser = localStorage.getItem("user");
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem("user");
    setUser(null);
  };

  const handleRegisterSuccess = () => {
    setShowRegister(false);
  };

  const renderCurrentPage = () => {
    switch (currentPage) {
      case "preferences":
        return <Preferences user={user} />;
      case "recipes_all":
        return <RecipesAll user={user} />;
      default:
        return <Preferences user={user} />;
    }
  };

  if (user) {
    return (
      <div className="min-h-screen bg-gray-50">
        <NavigationBar
          user={user}
          onLogout={handleLogout}
          currentPage={currentPage}
          onNavigate={setCurrentPage}
        />
        <div className="w-full py-8">{renderCurrentPage()}</div>
      </div>
    );
  }

  return (
    <div>
      <div className="bg-red-400 rounded-xl text-white p-4 text-center">
        <h1 className="text-2xl font-bold">🍓 BiteBerry</h1>
        <p className="text-red-100">Your personalized recipe assistant</p>
      </div>

      <div className="p-4">
        {showRegister ? (
          <div>
            <Register onRegister={handleRegisterSuccess} />
            <div className="text-center mt-4">
              <p className="text-gray-600">
                Already have an account?{" "}
                <button
                  onClick={() => setShowRegister(false)}
                  className="text-blue-500 hover:underline"
                >
                  Login here
                </button>
              </p>
            </div>
          </div>
        ) : (
          <div>
            <Login onLogin={handleLogin} />
            <div className="text-center mt-4">
              <p className="text-gray-600">
                Don't have an account?{" "}
                <button
                  onClick={() => setShowRegister(true)}
                  className="text-blue-500 hover:underline"
                >
                  Register here
                </button>
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AuthWrapper;
