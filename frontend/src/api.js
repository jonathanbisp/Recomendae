import axios from "axios";


const api = axios.create({
  baseURL: "http://localhost:3000",
});

api.interceptors.request.use(async config => {
  // Declaramos um token manualmente para teste.
  const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InN0cmluZyIsImV4cCI6MTY4OTI5ODU3OCwic3ViIjoiYWNjZXNzIn0.sUYPUBtTyx6TKB7oRyH1yMsM3GscoIhVbLfAQHozYBc";

  if (token) {
    api.defaults.headers.authorization = `Token ${token}`;
  }

  return config;
});

export default api;