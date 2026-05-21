import { Link, useLocation } from "react-router-dom"
import { Home, FlaskConical, Database } from "lucide-react"

export const Sidebar = () => {
  const location = useLocation()

  const isActive = (path: string) => location.pathname === path

  const linkClass = (active: boolean) =>
    `flex items-center gap-2 px-3 py-2 rounded-xl transition ${
      active ? "bg-zinc-800 text-white" : "text-zinc-400 hover:text-white hover:bg-zinc-900"
    }`

  return (
      <aside className="w-64 border-r border-zinc-800 bg-zinc-950 p-4">
        <div className="mb-6 text-zinc-500 text-sm">Navigation</div>

        <nav className="flex flex-col gap-2">
          {/* Путь к главной */}
          <Link to="/" className={linkClass(isActive("/"))}>
            <Home size={18} />
            Dashboard
          </Link>

          {/* ПУТЬ ИСПРАВЛЕН: был /generation, стал /generate */}
          <Link to="/generate" className={linkClass(isActive("/generate"))}>
            <FlaskConical size={18} />
            Generation
          </Link>

          <Link to="/experiments" className={linkClass(isActive("/experiments"))}>
            <Database size={18} />
            Experiments
          </Link>
        </nav>
      </aside>
    )
  }