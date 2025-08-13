import axios from "./axios";

export const getShoppingLists = async (userId) => {
  const res_list = await axios.get(`/shopping/lists?user_id=${userId}`);
  return res_list.data;
};

export const getShoppingListDetail = async (list_id) => {
  const res_detail = await axios.get(`/shopping/lists/${list_id}`);
  return res_detail.data;
};

export const toggleItem = async (item_id) => {
  const res_item = await axios.patch(`/shopping/items/${item_id}/toggle`);
  return res_item.data;
};

export const deleteShoppingList = async (list_id, userId) => {
  const res_list = await axios.delete(`/shopping/lists/${list_id}?user_id=${userId}`);
  return res_list.data;
};

export const createShoppingList = async (userId, listData) => {
  const res_list = await axios.post(`/shopping/lists?user_id=${userId}`, listData);
  return res_list.data;
};

export const createShoppingListFromMealPlans = async (userId, startDate, endDate, listName = "Weekly Shopping List") => {
  const response = await axios.post(`/shopping/from-meal-plans?user_id=${userId}&start_date=${startDate}&end_date=${endDate}&list_name=${encodeURIComponent(listName)}`);
  return response.data;
};
