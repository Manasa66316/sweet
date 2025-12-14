import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Protected from "../pages/Protected";
import ProtectedRoute from "./ProtectedRoute";

export default function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />

        <Route
          path="/protected"
          element={
            <ProtectedRoute>
              <Protected />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}
