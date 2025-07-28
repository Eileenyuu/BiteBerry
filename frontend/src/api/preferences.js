import axios from "./axios";

export const getUserPreferences = async () => {
  const res_prefs = await axios.get("api/preferences");
  return res_prefs.data;
};

export const updateUserPreferences = async (preferences) => {
  const res_prefs = await axios.put("api/preferences", preferences);
  return res_prefs.data;
};
