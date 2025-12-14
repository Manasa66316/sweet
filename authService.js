import api from "../api/axios";

export const registerUser = async (data) => {
  const response = await api.post("/auth/register", data);
  return response.data;
};

export const loginUser = async (data) => {
  const response = await api.post("/auth/login", data);
  localStorage.setItem("token", response.data.access_token);
  return response.data;
};

export const logout = () => {
  localStorage.removeItem("token");
};
