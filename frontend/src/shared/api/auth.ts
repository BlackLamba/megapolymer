import { api } from "./client"

export type AuthResponse = {
  access_token: string
  token_type: string
}

export type LoginDTO = {
  email: string
  password: string
}

export type RegisterDTO = {
  email: string
  password: string
}

export const login = async (data: LoginDTO): Promise<AuthResponse> => {
  const res = await api.post("/auth/login", data)
  return res.data
}

export const register = async (data: RegisterDTO) => {
  const res = await api.post("/auth/register", data)
  return res.data
}