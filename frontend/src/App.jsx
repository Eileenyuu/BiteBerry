import { useEffect, useState } from "react";
import "./App.css";

function App() {
  // State management for form inputs and results
  const [budget, setBudget] = useState(10);
  const [cookingTime, setCookingTime] = useState(30);
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Function to fetch recommendations from the backend
  const getRecommendations = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(
        `http://localhost:8000/recommend?max_budget=${budget}&max_cooking_time=${cookingTime}`,
        {
          method: "GET",
        }
      );
      if (!response.ok) {
        throw new Error("Failed to fetch recommendations");
      }

      const data = await response.json();
      setRecipes(data.recommendations || []);
    } catch (error) {
      console.error("Error: ", error);
      setError(
        "Fetch recommendation failed, please make sure backend is running"
      );
    } finally {
      setLoading(false);
    }
  };

  // Fetch recommendations on component mount
  useEffect(() => {
    getRecommendations();
  }, []); //Empty dependency array means this runs once on mount

  return (
    <>
      <h1>🍓 BiteBerry - Test Page</h1>

      <div className="card">
        <label>
          Budget: £
          <input
            type="number"
            value={budget}
            onChange={(e) => setBudget(e.target.value)}
            min="1"
            max="50"
          />
        </label>
        <label>
          Cooking Time:
          <input
            type="number"
            value={cookingTime}
            onChange={(e) => setCookingTime(e.target.value)}
            min="10"
            max="90"
          />{" "}
          min
        </label>

        <button onClick={getRecommendations} disabled={loading}>
          {loading ? "Loading..." : "Get Recommendations"}
        </button>
      </div>

      {/* Error display */}
      {error && (
        <div className="error" style={{ color: "red", margin: "20px 0" }}>
          {error}
        </div>
      )}

      {/* Results display */}
      {recipes.length > 0 && (
        <div className="results">
          <h2>Recipe Recommendations</h2>
          <div className="recipes-grid">
            {recipes.map((recipe, index) => (
              <div
                key={index}
                className="recipe-card"
                style={{
                  border: "1px solid #ccc",
                  padding: "15px",
                  margin: "10px 0",
                  borderRadius: "8px",
                }}
              >
                <h3>{recipe.title}</h3>
                <p>
                  <strong>Budget:</strong> £{recipe.budget}
                </p>
                <p>
                  <strong>Cooking Time:</strong> {recipe.cooking_time} minutes
                </p>
                <p>
                  <strong>Description: </strong>
                  {recipe.description}
                </p>
                {recipe.ingredients && (
                  <div>
                    <strong>Ingredients:</strong>
                    <ul>
                      {recipe.ingredients.map((ingredient, i) => (
                        <li key={i}>{ingredient}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </>
  );
}

export default App;
