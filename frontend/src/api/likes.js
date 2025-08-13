import axios from "./axios";

export const likeRecipe = async (recipeId, userId) => {
  const response = await axios.post(`/api/recipes/${recipeId}/like/${userId}`);
  return response.data;
};

export const getRecipeLikeInfo = async (recipeId, userId) => {
  const response = await axios.get(`/api/recipes/${recipeId}/likes/${userId}`);
  return response.data;
};

export const unlikeRecipe = async (recipeId, userId) => {
  const response = await axios.delete(`/api/recipes/${recipeId}/unlike/${userId}`);
  return response.data;
};

export const getUserLikedRecipes = async (userId) => {
  const response = await axios.get(`/api/recipes/liked/${userId}`);
  return response.data;
};