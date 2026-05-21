import { useState } from "react"
import { useExperimentPolling } from "@/shared/hooks/useExperimentPolling"

export const GeneratePanel = () => {
  const [id, setId] = useState<number | null>(null)
  const experiment = useExperimentPolling(id)

  const generate = async () => {
    // Исправлен URL: добавлен префикс /generation
    const res = await fetch("http://localhost:8000/generation/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        tg: 100,
        td: 350,
        cp: 1.5,
        tsb: 50,
        ym: 2.5,
        rho: 1.2,
        num_samples: 20
      }),
    })

    const data = await res.json()
    setId(data.experiment_id)
  }

  return (
    <div className="space-y-4">
      <button
        onClick={generate}
        className="px-4 py-2 rounded-xl bg-green-600 text-white font-medium hover:bg-green-700 transition"
      >
        Quick Test (20 Samples)
      </button>

      {experiment && (
        <div className="p-4 rounded-xl bg-zinc-900 border border-zinc-800 space-y-3">
          <p className="text-sm text-zinc-500">
            Experiment #{experiment.id}
          </p>

          {experiment.status === "processing" && (
            <p className="text-yellow-400 animate-pulse flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-yellow-400 animate-ping" />
              AI is building polymer chains...
            </p>
          )}

          {experiment.status === "done" && (
            <div className="space-y-3">
              <p className="text-green-400 font-semibold">Generation complete!</p>
              
              {/* Рендерим массив сгенерированных молекул */}
              <div className="max-h-60 overflow-y-auto space-y-2 pr-2 custom-scrollbar">
                {experiment.molecules?.map((mol: any, index: number) => (
                  <div key={index} className="p-2 rounded-lg bg-zinc-950 border border-zinc-800 text-xs flex justify-between items-center gap-4">
                    <span className="font-mono text-zinc-300 break-all select-all">{mol.smiles}</span>
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase shrink-0 ${
                      mol.valid ? "bg-green-950 text-green-400 border border-green-800" : "bg-red-950 text-red-400 border border-red-800"
                    }`}>
                      {mol.valid ? "valid" : "invalid"}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}