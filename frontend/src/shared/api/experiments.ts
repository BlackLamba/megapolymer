import { api } from "./client"

export interface MoleculeResult {
  id: number
  smiles: string
  valid: boolean
  predicted_tg?: number | null
}

export interface Experiment {
  id: number
  status: string
  
  // Актуальные 6 физических параметров полимера
  tg: number
  td: number
  cp: number
  tsb: number
  ym: number
  rho: number

  // Массив сгенерированных молекул (все 20 сэмплов)
  molecules: MoleculeResult[]
}

export const getExperiments = async (): Promise<Experiment[]> => {
  const res = await api.get<Experiment[]>("/experiments")
  return res.data
}

export const getExperiment = async (id: number): Promise<Experiment> => {
  const res = await api.get<Experiment>(`/experiments/${id}`)
  return res.data
}