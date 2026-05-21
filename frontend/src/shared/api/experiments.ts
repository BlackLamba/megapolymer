import { api } from "./client"

export interface Experiment {
  id: number
  tg: number
  mw: number
  density: number
  smiles: string | null
  valid: boolean | null
  predicted_tg: number | null

  status?: string
}

export const getExperiments = async (): Promise<Experiment[]> => {
  const res = await api.get("/experiments")
  return res.data
}

export const getExperiment = async (id: number): Promise<Experiment> => {
  const res = await api.get(`/experiments/${id}`)
  return res.data
}