import { api } from "./client"

export interface GenerateRequest {
  tg: number
  td: number
  cp: number
  tsb: number
  ym: number
  rho: number
  num_samples?: number
}

export interface MoleculeResult {
  id?: number
  smiles: string
  valid: boolean
  predicted_tg?: number
}

export interface GenerateResponse {
  experiment_id: number
  status: string
  count: number
  results: MoleculeResult[] // <-- Бэкенд возвращает именно "results" при POST-запросе
}

export const generatePolymer = async (data: GenerateRequest) => {
  // Исправлен путь на "/generation/generate"
  const res = await api.post<GenerateResponse>("/generation/generate", data)
  return res.data
}