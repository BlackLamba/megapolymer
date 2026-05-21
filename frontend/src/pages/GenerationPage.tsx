import { useState } from "react"
import { Container } from "@/shared/ui/Container"
import { generatePolymer } from "@/shared/api/generation"

export const GenerationPage = () => {
  // Устанавливаем базовые физически адекватные дефолты
  const [tg, setTg] = useState("100")
  const [td, setTd] = useState("350")
  const [cp, setCp] = useState("1.5")
  const [tsb, setTsb] = useState("50")
  const [ym, setYm] = useState("2.5")
  const [rho, setRho] = useState("1.2")
  
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)

  const handleGenerate = async () => {
    setLoading(true)
    try {
      const data = await generatePolymer({
        tg: Number(tg),
        td: Number(td),
        cp: Number(cp),
        tsb: Number(tsb),
        ym: Number(ym),
        rho: Number(rho),
        num_samples: 20 // Запрашиваем пачку из 20 молекул
      })
      setResult(data)
    } catch (e: any) {
      console.error(e)
      alert("Generation failed: " + (e.response?.data?.message || "Unknown error"))
    } finally {
      setLoading(false)
    }
  }
  
  return (
    <Container>
      <div className="space-y-8">
        <div>
          <h1 className="text-3xl font-bold">Polymer Generation</h1>
          <p className="text-zinc-400 text-sm mt-1">Specify target parameters to generate custom molecular structures.</p>
        </div>

        {/* СЕТКА ИНПУТОВ ИЗ 6 ПАРАМЕТРОВ */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div className="flex flex-col gap-1.5">
            <label className="text-xs text-zinc-400 font-medium">Glass Transition Temp (Tg), °C</label>
            <input
              className="bg-zinc-900 p-3 rounded-xl border border-zinc-800 text-white focus:outline-none focus:border-zinc-700"
              placeholder="e.g. 100"
              value={tg}
              onChange={(e) => setTg(e.target.value)}
            />
            <span className="text-[10px] text-zinc-500">Typical range: -100 to 300 °C</span>
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-xs text-zinc-400 font-medium">Decomposition Temp (Td), °C</label>
            <input
              className="bg-zinc-900 p-3 rounded-xl border border-zinc-800 text-white focus:outline-none focus:border-zinc-700"
              placeholder="e.g. 350"
              value={td}
              onChange={(e) => setTd(e.target.value)}
            />
            <span className="text-[10px] text-zinc-500">Typical range: 200 to 500 °C</span>
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-xs text-zinc-400 font-medium">Heat Capacity (Cp), J/(g·K)</label>
            <input
              className="bg-zinc-900 p-3 rounded-xl border border-zinc-800 text-white focus:outline-none focus:border-zinc-700"
              placeholder="e.g. 1.5"
              value={cp}
              onChange={(e) => setCp(e.target.value)}
            />
            <span className="text-[10px] text-zinc-500">Typical range: 1.0 to 2.5 J/(g·K)</span>
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-xs text-zinc-400 font-medium">Tensile Strength at Break (Tsb), MPa</label>
            <input
              className="bg-zinc-900 p-3 rounded-xl border border-zinc-800 text-white focus:outline-none focus:border-zinc-700"
              placeholder="e.g. 50"
              value={tsb}
              onChange={(e) => setTsb(e.target.value)}
            />
            <span className="text-[10px] text-zinc-500">Typical range: 10 to 100 MPa</span>
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-xs text-zinc-400 font-medium">Young's Modulus (Ym), GPa</label>
            <input
              className="bg-zinc-900 p-3 rounded-xl border border-zinc-800 text-white focus:outline-none focus:border-zinc-700"
              placeholder="e.g. 2.5"
              value={ym}
              onChange={(e) => setYm(e.target.value)}
            />
            <span className="text-[10px] text-zinc-500">Typical range: 0.1 to 10.0 GPa</span>
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-xs text-zinc-400 font-medium">Density (Rho), g/cm³</label>
            <input
              className="bg-zinc-900 p-3 rounded-xl border border-zinc-800 text-white focus:outline-none focus:border-zinc-700"
              placeholder="e.g. 1.2"
              value={rho}
              onChange={(e) => setRho(e.target.value)}
            />
            <span className="text-[10px] text-zinc-500">Typical range: 0.8 to 2.0 g/cm³</span>
          </div>
        </div>

        {/* КНОПКА ЗАПУСКА */}
        <button
          onClick={handleGenerate}
          disabled={loading}
          className="bg-white text-black px-6 py-3 rounded-xl font-semibold hover:bg-zinc-200 transition disabled:opacity-50"
        >
          {loading ? "AI is running simulation..." : "Generate Polymer Candidates"}
        </button>

        {/* БЛОК С РЕЗУЛЬТАТАМИ ТЕСТА */}
        <div className="mt-10 p-6 rounded-2xl bg-zinc-900 border border-zinc-800">
          <h3 className="text-lg font-semibold mb-4 text-zinc-200">Generated Molecules Stack</h3>
          
          {!result && (
            <p className="text-zinc-500 text-sm">
              Enter physical properties above and hit generate to query the latent space.
            </p>
          )}

          {result && (
            <div className="grid grid-cols-1 gap-3 max-h-[500px] overflow-y-auto pr-2 custom-scrollbar">
              {result.results?.map((mol: any, index: number) => ( // <-- Изменено на .results
                <div key={index} className="p-4 rounded-xl bg-zinc-950 border border-zinc-800 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                  <div className="space-y-1 min-w-0">
                    <span className="text-[10px] text-zinc-500 uppercase tracking-wider font-semibold">Candidate #{index + 1}</span>
                    <p className="text-white font-mono text-sm break-all select-all">{mol.smiles}</p>
                  </div>
                  
                  <div className="flex items-center gap-3 shrink-0">
                    <span className={`px-2.5 py-1 rounded-lg text-xs font-bold uppercase tracking-wide border ${
                      mol.valid 
                        ? "bg-green-950/50 text-green-400 border-green-800/60" 
                        : "bg-red-950/50 text-red-400 border-red-800/60"
                    }`}>
                      {mol.valid ? "SMILES Valid" : "Invalid Structure"}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </Container>
  )
}