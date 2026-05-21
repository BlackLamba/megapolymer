import { useState } from "react"

import { login } from "@/shared/api/auth"
import { auth } from "@/shared/lib/auth"

interface Props {
  open: boolean
  onClose: () => void
}

export const LoginModal = ({
  open,
  onClose
}: Props) => {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  if (!open) return null

  const handleLogin = async () => {
    try {
      const res = await login({
        email,
        password
      })

      auth.setAuth(res.access_token, email)

      onClose()

      window.location.reload()
    } catch (e) {
      console.error(e)
    }
  }

  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50">

      <div className="w-96 rounded-3xl bg-zinc-900 border border-zinc-800 p-6 space-y-4">

        <h2 className="text-2xl font-bold">
          Login
        </h2>

        <input
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full p-3 rounded-xl bg-zinc-800 outline-none"
        />

        <input
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full p-3 rounded-xl bg-zinc-800 outline-none"
        />

        <button
          onClick={handleLogin}
          className="w-full py-3 rounded-xl bg-blue-500 hover:bg-blue-400 transition"
        >
          Login
        </button>

      </div>

    </div>
  )
}