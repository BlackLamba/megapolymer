import { api } from "./client"

export interface GenerateRequest {
  tg: number
  mw: number
  density: number
}

export interface GenerateResponse {
  smiles: string
  valid: boolean
  predicted_tg?: number
}

export const generatePolymer = async (data: GenerateRequest) => {
  const res = await api.post<GenerateResponse>("/generate", data)
  return res.data
}