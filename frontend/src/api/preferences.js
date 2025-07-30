import axios from "./axios";

export const getUserPreferences = async (userId) => {
  const res_prefs = await axios.get(`/api/preferences/${userId}`);
  return res_prefs.data;
};

export const updateUserPreferences = async (userId, preferences) => {
  const res_prefs = await axios.put(`/api/preferences/${userId}`, preferences);
  return res_prefs.data;
};
