import { useEffect, useState } from "react";
import { getUserPreferences, updateUserPreferences } from "../api/preferences";
import { getRecommendations } from "../api/recipes";

const Preferences = () => {
  const [prefs, setPrefs] = useState({
    max_budget: "",
    max_cooking_time: "",
    dietary_restrictions: null,
  });
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);
  const [recipes, setRecipes] = useState([]);

  useEffect(() => {
    // Loading user preferences on initialization
    const fetchUserPreferences = async () => {
      try {
        const prefs = await getUserPreferences();
        setPrefs(prefs);
      } catch (error) {
        console.error("Failed to load preferences:", error);
      }
    };
    fetchUserPreferences();
  }, []);

  // Handling form submit
  const handleSubmitPrefs = async (e) => {
    e.preventDefault();
    setLoading(true);
    setStatus("");

    try {
      await updateUserPreferences(prefs);
      setStatus("Your preferences saved successfully!");

      // Get recipe recommendations using current form values
      const response = await getRecommendations({
        max_budget: parseFloat(prefs.max_budget),
        max_cooking_time: parseInt(prefs.max_cooking_time),
      });
      setRecipes(response.recommendations || []);
    } catch (error) {
      setStatus("Failed to save your preferences. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setPrefs((pref) => ({
      ...pref,
      [name]: value,
    }));
  };

  return (
    <div className="preferences-container">
      <h1>🍓 Your Preferences</h1>

      <form onSubmit={handleSubmitPrefs}>
        {/* Budget Input */}
        <div className="budgetBox mt-3">
          <label htmlFor="max_budget">Budget: £</label>
          <input
            type="number"
            id="max_budget"
            name="max_budget"
            value={prefs.max_budget}
            onChange={handleInputChange}
            min="1"
            max="100"
            step="0.01"
            placeholder="Enter maximum budget"
          />
        </div>

        {/* Cooking Time Input */}
        <div className="cookingTimeBox mt-3">
          <label htmlFor="max_cooking_time">Cooking Time: </label>
          <input
            type="number"
            id="max_cooking_time"
            name="max_cooking_time"
            value={prefs.max_cooking_time}
            onChange={handleInputChange}
            min="10"
            max="180"
            placeholder="Enter maximum cooking time"
          />{" "}
          mins
        </div>

        {/* Dietary restriction selection */}
        <div className="cookingTimeBox mt-3">
          <label htmlFor="dietary_restrictions">Dietary Restrictions:</label>
          <select
            id="dietary_restrictions"
            name="dietary_restrictions"
            value={prefs.dietary_restrictions || ""}
            onChange={handleInputChange}
          >
            <option value="">No restrictions</option>
            <option value="vegetarian">Vegetarian</option>
            <option value="vegan">Vegan</option>
            <option value="gluten-free">Gluten Free</option>
            <option value="dairy-free">Dairy Free</option>
            <option value="keto">Keto</option>
          </select>
        </div>

        <button className="saveButton mt-3" type="submit" disabled={loading}>
          {loading ? "Saving..." : "Save Preferences"}
        </button>

        {/* Status Message */}
        {status && (
          <div
            style={{
              marginTop: "10px",
              padding: "10px",
              borderRadius: "5px",
              backgroundColor: status.includes("successfully")
                ? "#d4edda"
                : "#f8d7da",
              border: `1px solid ${
                status.includes("successfully") ? "#c3e6cb" : "#f5c6cb"
              }`,
              color: status.includes("successfully") ? "#155724" : "#721c24",
            }}
          >
            {status}
          </div>
        )}
      </form>

      {/* Recipe Recommendations Section */}
      {recipes.length > 0 ? (
        <div className="results" style={{ marginTop: "30px" }}>
          <h2>🍽️ Recipe Recommendations</h2>
          <div className="recipes-grid">
            {recipes.map((recipe, index) => (
              <div
                key={recipe.recipe_id || index}
                className="recipe-card"
                style={{
                  border: "1px solid #ccc",
                  padding: "15px",
                  margin: "10px 0",
                  borderRadius: "8px",
                  backgroundColor: "#f9f9f9",
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
                  <strong>Description:</strong> {recipe.description}
                </p>
                {recipe.cuisine && (
                  <p>
                    <strong>Cuisine:</strong> {recipe.cuisine}
                  </p>
                )}
                {recipe.ingredients && (
                  <div>
                    <strong>Ingredients:</strong>
                    <ul style={{ marginTop: "5px" }}>
                      {Array.isArray(recipe.ingredients) ? (
                        recipe.ingredients.map((ingredient, i) => (
                          <li key={i}>{ingredient}</li>
                        ))
                      ) : (
                        <li>{recipe.ingredients}</li>
                      )}
                    </ul>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div
          style={{
            marginTop: "30px",
            padding: "15px",
            backgroundColor: "#fff3cd",
            border: "1px solid #ffeaa7",
            borderRadius: "5px",
          }}
        >
          <p>
            💡 <strong>No recipes found yet.</strong>
          </p>
          <p>
            Fill in your preferences above and click "Save Preferences" to get
            personalized recipe recommendations!
          </p>
        </div>
      )}
    </div>
  );
};

export default Preferences;
