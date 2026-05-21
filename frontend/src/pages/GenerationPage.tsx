import { useState } from "react"
import { Container } from "@/shared/ui/Container"
import { generatePolymer } from "@/shared/api/generation"

export const GenerationPage = () => {
  const [tg, setTg] = useState("")
  const [mw, setMw] = useState("")
  const [density, setDensity] = useState("")
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)

  const handleGenerate = async () => {
    setLoading(true)
    try {
      const data = await generatePolymer({
        tg: Number(tg),
        mw: Number(mw),
        density: Number(density),
      })
      setResult(data)
    } catch (e: any) {
      console.error(e)
      // Теперь здесь не будет ложного "не авторизован", 
      // так как 401 перехватывается в client.ts
      alert("Generation failed: " + (e.response?.data?.message || "Unknown error"))
    } finally {
      setLoading(false)
    }
  }
  
  return (
    <Container>
      <div className="space-y-8">
        <h1 className="text-3xl font-bold">
          Polymer Generation
        </h1>

        {/* INPUTS */}
        <div className="grid grid-cols-3 gap-4">
          <input
            className="bg-zinc-900 p-3 rounded-xl border border-zinc-800"
            placeholder="Tg"
            value={tg}
            onChange={(e) => setTg(e.target.value)}
          />

          <input
            className="bg-zinc-900 p-3 rounded-xl border border-zinc-800"
            placeholder="Molecular Weight"
            value={mw}
            onChange={(e) => setMw(e.target.value)}
          />

          <input
            className="bg-zinc-900 p-3 rounded-xl border border-zinc-800"
            placeholder="Density"
            value={density}
            onChange={(e) => setDensity(e.target.value)}
          />
        </div>

        {/* BUTTON */}
        <button
          onClick={handleGenerate}
          disabled={loading}
          className="bg-white text-black px-6 py-3 rounded-xl font-semibold hover:bg-zinc-200 transition disabled:opacity-50"
        >
          {loading ? "Generating..." : "Generate Polymer"}
        </button>

        {/* RESULT */}
        <div className="mt-10 p-6 rounded-2xl bg-zinc-900 border border-zinc-800">
          {!result && (
            <p className="text-zinc-400">
              Generated molecule will appear here...
            </p>
          )}

          {result && (
            <div className="space-y-3">
              <div>
                <span className="text-zinc-400">SMILES:</span>
                <p className="text-white font-mono">{result.smiles}</p>
              </div>

              <div>
                <span className="text-zinc-400">Valid:</span>
                <p className={result.valid ? "text-green-400" : "text-red-400"}>
                  {String(result.valid)}
                </p>
              </div>

              {result.predicted_tg && (
                <div>
                  <span className="text-zinc-400">Predicted Tg:</span>
                  <p>{result.predicted_tg}</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </Container>
  )
}