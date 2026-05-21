import { useState } from "react"

import { auth } from "@/shared/lib/auth"

import { LoginModal } from "@/features/auth/LoginModal"
import { RegisterModal } from "@/features/auth/RegisterModal"

export const TopBar = () => {
  const [loginOpen, setLoginOpen] = useState(false)
  const [registerOpen, setRegisterOpen] = useState(false)

  const isAuth = auth.isAuthenticated()

  return (
    <>
      <div className="border-b border-zinc-800 bg-black/80 backdrop-blur">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">

          <div>
            <h1 className="text-xl font-bold text-white">
              Polymer AI Platform
            </h1>
          </div>

          <div className="flex items-center gap-3">

            {isAuth ? (
              <>
                <div className="text-sm text-zinc-400">
                  {auth.getEmail()}
                </div>

                <button
                  onClick={() => {
                    auth.logout()
                    window.location.reload()
                  }}
                  className="px-4 py-2 rounded-xl bg-red-500/20 text-red-400 hover:bg-red-500/30 transition"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <button
                  onClick={() => setLoginOpen(true)}
                  className="px-4 py-2 rounded-xl bg-zinc-800 hover:bg-zinc-700 transition"
                >
                  Login
                </button>

                <button
                  onClick={() => setRegisterOpen(true)}
                  className="px-4 py-2 rounded-xl bg-blue-500 hover:bg-blue-400 transition"
                >
                  Register
                </button>
              </>
            )}

          </div>

        </div>
      </div>

      <LoginModal
        open={loginOpen}
        onClose={() => setLoginOpen(false)}
      />

      <RegisterModal
        open={registerOpen}
        onClose={() => setRegisterOpen(false)}
      />
    </>
  )
}