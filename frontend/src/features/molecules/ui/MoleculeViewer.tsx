import { useEffect, useState } from "react"

interface Props {
  smiles: string
}

// Глобальные переменные, чтобы не инициализировать тяжелый 5MB WASM-модуль при каждом рендере карточки
let rdkitInstance: any = null
let rdkitLoadingPromise: Promise<any> | null = null

const initRDKitBackend = (): Promise<any> => {
  if (rdkitInstance) return Promise.resolve(rdkitInstance)
  if (rdkitLoadingPromise) return rdkitLoadingPromise

  rdkitLoadingPromise = new Promise((resolve, reject) => {
    // Если скрипт уже загружен в window
    if ((window as any).initRDKitModule) {
      (window as any).initRDKitModule()
        .then((RDKit: any) => {
          rdkitInstance = RDKit
          resolve(RDKit)
        })
        .catch(reject)
      return
    }

    // Динамически инжектим официальный WASM-бандл RDKit
    const script = document.createElement("script")
    script.src = "https://unpkg.com/@rdkit/rdkit/dist/RDKit_minimal.js"
    script.async = true
    script.onload = () => {
      (window as any).initRDKitModule()
        .then((RDKit: any) => {
          rdkitInstance = RDKit
          resolve(RDKit)
        })
        .catch(reject)
    }
    script.onerror = () => reject(new Error("RDKit CDN load failed"))
    document.head.appendChild(script)
  })

  return rdkitLoadingPromise
}

export const MoleculeViewer = ({ smiles }: Props) => {
  const [svg, setSvg] = useState<string>("")
  const [isError, setIsError] = useState(false)

  useEffect(() => {
    let isMounted = true
    if (!smiles) return

    initRDKitBackend()
      .then((RDKit) => {
        if (!isMounted) return
        try {
          // Парсим SMILES силами оригинального ядра RDKit
          const mol = RDKit.get_mol(smiles)
          
          if (mol) {
            // Генерируем чистый векторный SVG
            const moleculeSvg = mol.get_svg()
            setSvg(moleculeSvg)
            setIsError(false)
            
            // ВАЖНО: Обязательно чистим память в WASM, иначе вкладка браузера быстро упадет от утечки памяти!
            mol.delete()
          } else {
            setIsError(true)
          }
        } catch (err) {
          console.error("RDKit parsing error:", err)
          setIsError(true)
        }
      })
      .catch((err) => {
        console.error("RDKit init error:", err)
        if (isMounted) setIsError(true)
      })

    return () => {
      isMounted = false
    }
  }, [smiles])

  if (isError) {
    return (
      <div className="w-[180px] h-[120px] flex items-center justify-center rounded-xl bg-red-950/20 border border-red-900/30">
        <span className="text-[10px] text-red-400 font-mono text-center px-2">Invalide Structure</span>
      </div>
    )
  }

  if (!svg) {
    return (
      <div className="w-[180px] h-[120px] bg-zinc-950 rounded-xl border border-zinc-800/60 animate-pulse flex items-center justify-center">
        <span className="text-[10px] text-zinc-600 font-mono">Rendering...</span>
      </div>
    )
  }

  return (
    <div 
      className="w-[180px] h-[120px] flex items-center justify-center p-1 rounded-xl bg-zinc-950/20 border border-zinc-800/40 custom-rdkit-container"
      dangerouslySetInnerHTML={{ __html: svg }}
    />
  )
}