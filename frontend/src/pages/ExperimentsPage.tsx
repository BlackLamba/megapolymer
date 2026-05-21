import { useEffect, useMemo, useState } from "react"
import { useNavigate } from "react-router-dom"

import { auth } from "@/shared/lib/auth"
import { Container } from "@/shared/ui/Container"
import { GeneratePanel } from "@/features/generation/GeneratePanel"
import { MoleculeViewer } from "@/features/molecules/ui/MoleculeViewer"

import { getExperiments } from "@/shared/api/experiments"
import type { Experiment } from "@/shared/api/experiments"

export const ExperimentsPage = () => {
  const [data, setData] = useState<Experiment[]>([])
  const [loading, setLoading] = useState(true)

  const [search, setSearch] = useState("")
  const [sortBy, setSortBy] = useState<"newest" | "oldest" | "tg">("newest")

  const navigate = useNavigate()

  // 📡 LOAD FUNCTION
  const loadExperiments = async () => {
    try {
      const res = await getExperiments()
      setData(res)
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  // 🚀 Initial load
  useEffect(() => {
    loadExperiments()
  }, [])

  // 🔄 Polling for updates
  useEffect(() => {
    let active = true

    const interval = setInterval(async () => {
      if (!active) return
      await loadExperiments()
    }, 2000)

    return () => {
      active = false
      clearInterval(interval)
    }
  }, [])

  // 🔎 FILTERED BY NESTED MOLECULES
  const filteredData = useMemo(() => {
    if (!search.trim()) return data
    return data.filter((exp) =>
      exp.molecules?.some((mol) =>
        mol.smiles?.toLowerCase().includes(search.toLowerCase())
      )
    )
  }, [data, search])

  // 🔄 SORTED BY CHOSEN METRIC
  const sortedData = useMemo(() => {
    return [...filteredData].sort((a, b) => {
      if (sortBy === "newest") return b.id - a.id
      if (sortBy === "oldest") return a.id - b.id
      if (sortBy === "tg") return b.tg - a.tg
      return 0
    })
  }, [filteredData, sortBy])

  return (
    <Container>
      <div className="space-y-6">
        {/* HEADER */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">Experiments History</h1>
            <p className="text-zinc-500 mt-2">
              Stored polymer generation experiments and generated candidates
            </p>
          </div>
        </div>

        {/* GENERATION PANEL */}
        {auth.isAuthenticated() && <GeneratePanel />}

        {/* CONTROLS */}
        <div className="flex gap-4">
          <input
            placeholder="Search experiments by candidate SMILES..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="bg-zinc-900 border border-zinc-800 rounded-xl px-4 py-3 w-full outline-none focus:border-zinc-600 transition text-sm"
          />

          <select
            value={sortBy}
            onChange={(e) =>
              setSortBy(e.target.value as "newest" | "oldest" | "tg")
            }
            className="bg-zinc-900 border border-zinc-800 rounded-xl px-4 py-3 outline-none text-sm cursor-pointer text-zinc-300"
          >
            <option value="newest">Newest First</option>
            <option value="oldest">Oldest First</option>
            <option value="tg">Highest Target Tg</option>
          </select>
        </div>

        {/* LOADING */}
        {loading && (
          <div className="text-zinc-500 animate-pulse text-sm">
            Loading ML prediction history...
          </div>
        )}

        {/* EMPTY */}
        {!loading && sortedData.length === 0 && (
          <div className="text-zinc-500 text-sm bg-zinc-900/50 p-8 rounded-2xl text-center border border-zinc-800/40">
            No experiments found matching the criteria.
          </div>
        )}

        {/* EXPERIMENTS LIST */}
        <div className="grid gap-6">
          {sortedData.map((exp) => (
            <div
              key={exp.id}
              className="p-6 rounded-3xl bg-zinc-900 border border-zinc-800/80 space-y-6"
            >
              {/* TOP: EXPERIMENT INFO & TARGETS */}
              <div className="flex flex-col gap-4">
                <div className="flex justify-between items-center border-b border-zinc-800 pb-3">
                  <div>
                    <h3 className="text-white font-semibold">Experiment #{exp.id}</h3>
                    <p className="text-[11px] text-zinc-500">Condition Targets Matrix</p>
                  </div>
                  
                  {/* SYSTEM STATUS BADGE */}
                  <span className={`px-2.5 py-1 rounded-md text-[10px] font-bold uppercase tracking-wider ${
                    exp.status === "done" ? "bg-green-950/40 text-green-400 border border-green-900/50" :
                    exp.status === "failed" ? "bg-red-950/40 text-red-400 border border-red-900/50" :
                    "bg-yellow-950/40 text-yellow-400 border border-yellow-900/50 animate-pulse"
                  }`}>
                    {exp.status}
                  </span>
                </div>

                {/* 6 PHYSICAL PROPERTIES GRID */}
                <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-4 p-4 rounded-2xl bg-zinc-950/40 border border-zinc-800/40 text-xs">
                  <div>
                    <p className="text-zinc-500 mb-0.5">Target Tg</p>
                    <p className="text-zinc-200 font-medium font-mono">{exp.tg} °C</p>
                  </div>
                  <div>
                    <p className="text-zinc-500 mb-0.5">Target Td</p>
                    <p className="text-zinc-200 font-medium font-mono">{exp.td} °C</p>
                  </div>
                  <div>
                    <p className="text-zinc-500 mb-0.5">Target Cp</p>
                    <p className="text-zinc-200 font-medium font-mono">{exp.cp}</p>
                  </div>
                  <div>
                    <p className="text-zinc-500 mb-0.5">Target TSb</p>
                    <p className="text-zinc-200 font-medium font-mono">{exp.tsb} MPa</p>
                  </div>
                  <div>
                    <p className="text-zinc-500 mb-0.5">Young's Mod.</p>
                    <p className="text-zinc-200 font-medium font-mono">{exp.ym} GPa</p>
                  </div>
                  <div>
                    <p className="text-zinc-500 mb-0.5">Density (ρ)</p>
                    <p className="text-zinc-200 font-medium font-mono">{exp.rho}</p>
                  </div>
                </div>
              </div>

              {/* BOTTOM: NESTED GENERATED CANDIDATES STACK */}
              {exp.status === "processing" && (
                <div className="p-4 rounded-xl bg-yellow-950/10 border border-yellow-900/20 text-yellow-500 text-xs animate-pulse flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-yellow-500 animate-ping" />
                  Generative model is currently sampling the latent space...
                </div>
              )}

              {exp.status === "failed" && (
                <div className="p-4 rounded-xl bg-red-950/10 border border-red-900/20 text-red-400 text-xs">
                  Critical error encountered during model inference pipeline.
                </div>
              )}

              {exp.status === "done" && exp.molecules && exp.molecules.length > 0 && (
                <div className="space-y-3">
                  <h4 className="text-[11px] font-bold text-zinc-400 uppercase tracking-wider">
                    Generated Compounds Stack ({exp.molecules.length})
                  </h4>
                  
                  {/* Сетка со сгенерированными структурами */}
                  <div className="grid grid-cols-1 xl:grid-cols-2 gap-3">
                    {exp.molecules.map((mol) => (
                      <div 
                        key={mol.id} 
                        className="p-4 rounded-2xl bg-zinc-950 border border-zinc-800/60 flex flex-col sm:flex-row gap-4 items-center justify-between"
                      >
                        <div className="space-y-2 min-w-0 flex-1 w-full">
                          <div className="flex flex-wrap items-center gap-2">
                            <span className={`px-2 py-0.5 rounded text-[9px] font-bold uppercase tracking-wide border ${
                              mol.valid 
                                ? "bg-green-950/60 text-green-400 border-green-800/50" 
                                : "bg-red-950/60 text-red-400 border-red-800/50"
                            }`}>
                              {mol.valid ? "SMILES Valid" : "Invalid Layout"}
                            </span>
                            
                            {mol.predicted_tg !== undefined && mol.predicted_tg !== null && (
                              <span className="text-[11px] text-zinc-400">
                                Pred. Tg: <strong className="text-zinc-200 font-mono">{mol.predicted_tg.toFixed(1)} °C</strong>
                              </span>
                            )}
                          </div>
                          
                          <p className="font-mono text-xs text-zinc-300 break-all select-all bg-zinc-900/40 p-2 rounded-lg border border-zinc-900">
                            {mol.smiles}
                          </p>
                        </div>
                        
                        {/* Рендеринг 2D структуры полимера */}
                        <div className="shrink-0 bg-white p-1 rounded-xl shadow-inner border border-zinc-800">
                          <MoleculeViewer smiles={mol.smiles} />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </Container>
  )
}