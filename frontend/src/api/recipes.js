import axios from "./axios";

export const getAllRecipes = async () => {
  const recipes_res = await axios.get("/recipes");
  return recipes_res.data;
};

export const getRecommendations = async (params = {}) => {
  const recommend_res = await axios.get("/recommend", { params });
  return recommend_res.data;
};
