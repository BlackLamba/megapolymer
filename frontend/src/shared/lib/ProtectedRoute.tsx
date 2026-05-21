import { Navigate, Outlet } from "react-router-dom";
import { auth } from "./auth";

export const ProtectedRoute = () => {
  return auth.isAuthenticated() ? <Outlet /> : <Navigate to="/login" replace />;
};