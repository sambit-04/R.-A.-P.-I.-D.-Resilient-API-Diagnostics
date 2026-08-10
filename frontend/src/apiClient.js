import axios from "axios";

const API = "http://127.0.0.1:5000/api";

const client = axios.create({ baseURL: API, timeout: 30000 });

client.interceptors.request.use(cfg => {
  const token = localStorage.getItem("jwt_token");
  if (token) cfg.headers.Authorization = `Bearer ${token}`;
  return cfg;
});

export const login = (u, p) => axios.post(`${API}/auth/login`, { username: u, password: p });
export const startTest = (data) => client.post("/test", data);
export const getStatus = id => client.get(`/status/${id}`);
export const getResult = id => client.get(`/result/${id}`);
export const getHistory = () => client.get("/history");

export default client;
