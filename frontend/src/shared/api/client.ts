import axios from "axios"
import { auth } from "../lib/auth"

export const api = axios.create({
  baseURL: "http://localhost:8000",
})

api.interceptors.request.use((config) => {
  const token = auth.getToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Опционально: глобальный обработчик ошибок
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      auth.logout()
      window.location.href = "/login" // Принудительный редирект
    }
    return Promise.reject(error)
  }
)