import type { ReactNode } from "react"

interface Props {
  children: ReactNode
}

export const Container = ({ children }: Props) => {
  return (
    <div className="max-w-7xl mx-auto w-full">
      {children}
    </div>
  )
}