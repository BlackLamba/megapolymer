import { createBrowserRouter, Navigate } from "react-router-dom"
import { MainLayout } from "@/app/layouts/MainLayout"
import { HomePage } from "@/pages/HomePage"
import { ExperimentsPage } from "@/pages/ExperimentsPage"
import { GenerationPage } from "@/pages/GenerationPage"
import { ProtectedRoute } from "@/shared/lib/ProtectedRoute"

export const router = createBrowserRouter([
  {
    path: "/",
    element: <MainLayout />,
    children: [
      { index: true, element: <HomePage /> },
      { path: "experiments", element: <ExperimentsPage /> },
      {
        element: <ProtectedRoute />,
        children: [
          { path: "generate", element: <GenerationPage /> },
        ],
      },
      { path: "*", element: <Navigate to="/" replace /> },
    ],
  },
])