import axios from "./axios";

export const registerUser = async (userData) => {
  const register_res = await axios.post("/api/register", userData);
  return register_res.data;
};

export const loginUser = async (loginData) => {
  const login_res = await axios.post("/api/login", loginData);
  return login_res.data;
};
