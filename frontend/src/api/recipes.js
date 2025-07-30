import axios from "./axios";

export const getAllRecipes = async () => {
  const recipes_res = await axios.get("/recipes");
  return recipes_res.data;
};

export const getRecommendations = async (userId, params = {}) => {
  const recommend_res = await axios.get(`/recommend/${userId}`, { params });
  return recommend_res.data;
};

export const getRecipeDetail = async (recipe_id) => {
  const recipeDetail_res = await axios.get(`/api/recipes/${recipe_id}`);
  return recipeDetail_res.data;
};
