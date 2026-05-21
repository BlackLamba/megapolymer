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

  const handleLogout = () => {
    auth.logout()
    navigate("/login")
  }

  // 📡 LOAD FUNCTION (reusable)
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

  // 🚀 initial load
  useEffect(() => {
    loadExperiments()
  }, [])

  // 🔄 polling (CLEAN VERSION)
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

  // 🔎 filtered + sorted (memoized)
  const filteredData = useMemo(() => {
    return data.filter((exp) =>
      exp.smiles?.toLowerCase().includes(search.toLowerCase())
    )
  }, [data, search])

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
            <h1 className="text-3xl font-bold">
              Experiments History
            </h1>

            <p className="text-zinc-500 mt-2">
              Stored polymer generation experiments
            </p>
          </div>
        </div>

        {/* GENERATION PANEL */}
        {auth.isAuthenticated() && (
          <GeneratePanel />
        )}

        {/* CONTROLS */}
        <div className="flex gap-4">
          <input
            placeholder="Search by SMILES..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="bg-zinc-900 border border-zinc-800 rounded-xl px-4 py-3 w-full outline-none focus:border-zinc-600 transition"
          />

          <select
            value={sortBy}
            onChange={(e) =>
              setSortBy(e.target.value as "newest" | "oldest" | "tg")
            }
            className="bg-zinc-900 border border-zinc-800 rounded-xl px-4 py-3 outline-none"
          >
            <option value="newest">Newest</option>
            <option value="oldest">Oldest</option>
            <option value="tg">Highest Tg</option>
          </select>
        </div>

        {/* LOADING */}
        {loading && (
          <div className="text-zinc-500 animate-pulse">
            Loading experiments...
          </div>
        )}

        {/* EMPTY */}
        {!loading && sortedData.length === 0 && (
          <div className="text-zinc-500">
            No experiments found
          </div>
        )}

        {/* LIST */}
        <div className="grid gap-4">
          {sortedData.map((exp) => (
            <div
              key={exp.id}
              className="group p-5 rounded-3xl bg-zinc-900 border border-zinc-800 hover:border-zinc-700 transition"
            >
              <div className="flex justify-between items-start">

                {/* LEFT */}
                <div className="space-y-3">

                  <div>
                    <p className="text-zinc-500 text-sm">
                      Experiment #{exp.id}
                    </p>

                    <p className="font-mono text-green-400 break-all mt-2">
                      {exp.smiles}
                    </p>
                  </div>

                  {/* MOLECULE */}
                  {exp.smiles && (
                    <MoleculeViewer smiles={exp.smiles} />
                  )}

                  <div className="flex gap-6 text-sm">
                    <div>
                      <p className="text-zinc-500">Tg</p>
                      <p className="text-white">{exp.tg}</p>
                    </div>

                    <div>
                      <p className="text-zinc-500">MW</p>
                      <p className="text-white">{exp.mw}</p>
                    </div>

                    <div>
                      <p className="text-zinc-500">Density</p>
                      <p className="text-white">{exp.density}</p>
                    </div>
                  </div>

                  {/* STATUS */}
                  {exp.status === "processing" && (
                    <div className="text-yellow-400 text-sm animate-pulse">
                      AI is generating molecule...
                    </div>
                  )}
                </div>

                {/* RIGHT */}
                <div className="text-right">

                  <div
                    className={`px-3 py-1 rounded-full text-sm ${
                      exp.valid
                        ? "bg-green-500/20 text-green-400"
                        : "bg-red-500/20 text-red-400"
                    }`}
                  >
                    {exp.valid ? "VALID" : "INVALID"}
                  </div>

                  <p className="mt-4 text-zinc-500 text-sm">
                    Predicted Tg
                  </p>

                  <p className="text-xl font-bold text-white">
                    {exp.predicted_tg?.toFixed(2)}
                  </p>
                </div>

              </div>
            </div>
          ))}
        </div>

      </div>
    </Container>
  )
}