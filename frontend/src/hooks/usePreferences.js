import { useState, useEffect } from "react";
import { getUserPreferences, updateUserPreferences } from "../api/preferences";
import { DIETARY_RESTRICTIONS, isValidDietaryRestriction } from "../constants/enums";

export const usePreferences = (user) => {
  const [prefs, setPrefs] = useState({
    max_budget: "",
    max_cooking_time: "",
    dietary_restrictions: DIETARY_RESTRICTIONS.NONE,
  });
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);

  // Load user preferences on initialization
  useEffect(() => {
    const fetchUserPreferences = async () => {
      if (!user?.id) return;

      try {
        const userPrefs = await getUserPreferences(user.id);
        setPrefs(userPrefs);
      } catch (error) {
        console.error("Failed to load preferences:", error);
      }
    };
    fetchUserPreferences();
  }, [user]);

  // Handle input changes with validation
  const handleInputChange = (e) => {
    const { name, value } = e.target;

    // Validate dietary restrictions
    if (name === "dietary_restrictions" && !isValidDietaryRestriction(value)) {
      console.warn(`Invalid dietary restriction value: ${value}`);
      return;
    }

    setPrefs((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  // Save preferences
  const savePreferences = async () => {
    if (!user?.id) return null;

    setLoading(true);
    setStatus("");

    try {
      await updateUserPreferences(user.id, prefs);
      setStatus("Your preferences saved successfully!");
      
      // Return parsed preferences for immediate use
      return {
        max_budget: parseFloat(prefs.max_budget),
        max_cooking_time: parseInt(prefs.max_cooking_time),
        dietary_restrictions: prefs.dietary_restrictions,
      };
    } catch {
      setStatus("Failed to save your preferences. Please try again.");
      return null;
    } finally {
      setLoading(false);
    }
  };

  return {
    prefs,
    status,
    loading,
    handleInputChange,
    savePreferences,
  };
};