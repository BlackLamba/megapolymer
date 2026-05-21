import { Outlet } from "react-router-dom"

import { TopBar } from "@/widgets/TopBar"
import { Sidebar } from "@/shared/ui/Sidebar"

export const MainLayout = () => {
  return (
    <div className="min-h-screen bg-zinc-900 text-white">

      <TopBar />

      <div className="flex">

        <Sidebar />

        <main className="flex-1 p-6">
          <Outlet />
        </main>

      </div>
    </div>
  )
}