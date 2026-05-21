import { useEffect, useRef } from "react"
import SmilesDrawer from "smiles-drawer"

interface Props {
  smiles: string
}

export const MoleculeViewer = ({ smiles }: Props) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null)

  useEffect(() => {
    if (!canvasRef.current) return

    const drawer = new SmilesDrawer.Drawer({
      width: 300,
      height: 200,
    })

    SmilesDrawer.parse(
      smiles,
      (tree: any) => {
        drawer.draw(tree, canvasRef.current!, "light", false)
      },
      (err: any) => {
        console.error(err)
      }
    )
  }, [smiles])

  return (
    <canvas
      ref={canvasRef}
      width={300}
      height={200}
      className="rounded-xl bg-white"
    />
  )
}