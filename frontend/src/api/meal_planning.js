import axios from "./axios";

export const addMealPlan = async (userId, mealPlanData) => {
  const response = await axios.post(`/meal-planning/plans?user_id=${userId}`, mealPlanData);
  return response.data;
};

export const getMealPlans = async (userId, startDate = null, endDate = null) => {
  let url = `/meal-planning/plans?user_id=${userId}`;
  
  if (startDate) {
    url += `&start_date=${startDate}`;
  }
  if (endDate) {
    url += `&end_date=${endDate}`;
  }
  
  const response = await axios.get(url);
  return response.data;
};

export const getWeeklyMealPlan = async (userId, weekStart) => {
  const response = await axios.get(`/meal-planning/weekly?user_id=${userId}&week_start=${weekStart}`);
  return response.data;
};

export const updateMealPlan = async (mealPlanId, userId, mealPlanData) => {
  const response = await axios.put(`/meal-planning/plans/${mealPlanId}?user_id=${userId}`, mealPlanData);
  return response.data;
};

export const deleteMealPlan = async (mealPlanId, userId) => {
  const response = await axios.delete(`/meal-planning/plans/${mealPlanId}?user_id=${userId}`);
  return response.data;
};