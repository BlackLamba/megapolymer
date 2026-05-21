import { useState } from "react"

import { register } from "@/shared/api/auth"

interface Props {
  open: boolean
  onClose: () => void
}

export const RegisterModal = ({
  open,
  onClose
}: Props) => {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  if (!open) return null

  const handleRegister = async () => {
    try {
      await register({
        email,
        password
      })

      onClose()
    } catch (e) {
      console.error(e)
    }
  }

  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50">

      <div className="w-96 rounded-3xl bg-zinc-900 border border-zinc-800 p-6 space-y-4">

        <h2 className="text-2xl font-bold">
          Register
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
          onClick={handleRegister}
          className="w-full py-3 rounded-xl bg-green-500 hover:bg-green-400 transition"
        >
          Register
        </button>

      </div>

    </div>
  )
}