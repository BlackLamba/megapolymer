import { useState } from "react"
import { useExperimentPolling } from "@/shared/hooks/useExperimentPolling"

export const GeneratePanel = () => {
  const [id, setId] = useState<number | null>(null)

  const experiment = useExperimentPolling(id)

  const generate = async () => {
    const res = await fetch("http://localhost:8000/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        tg: 120,
        mw: 500,
        density: 1.2,
      }),
    })

    const data = await res.json()
    setId(data.experiment_id)
  }

  return (
    <div className="space-y-4">

      <button
        onClick={generate}
        className="px-4 py-2 rounded-xl bg-green-600 text-white"
      >
        Generate molecule
      </button>

      {experiment && (
        <div className="p-4 rounded-xl bg-zinc-900 border border-zinc-800">

          <p className="text-sm text-zinc-500">
            Experiment #{experiment.id}
          </p>

          {experiment.status === "processing" && (
            <p className="text-yellow-400 animate-pulse">
              AI is thinking...
            </p>
          )}

          {experiment.status === "done" && (
            <>
              <p className="text-green-400">Done</p>

              <p className="font-mono text-green-300 break-all">
                {experiment.smiles}
              </p>
            </>
          )}

        </div>
      )}

    </div>
  )
}