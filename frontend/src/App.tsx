import type { ReactNode } from 'react'
import { useQueryClient } from '@tanstack/react-query'
import { Navigate, NavLink, Route, Routes, useLocation, useNavigate } from 'react-router'
import { auth } from './api'
import DevicesPage from './pages/DevicesPage'
import HealthPage from './pages/HealthPage'
import LoginPage from './pages/LoginPage'

function RequireAuth({ children }: { children: ReactNode }) {
  return auth.get() ? <>{children}</> : <Navigate to="/login" replace />
}

export default function App() {
  useLocation() // re-render on navigation so the header reflects login state
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const loggedIn = !!auth.get()

  const logout = () => {
    auth.clear()
    queryClient.clear()
    navigate('/login')
  }

  return (
    <>
      <header>
        <strong>NetOps Portal</strong>
        {loggedIn && (
          <>
            <NavLink to="/" end>Devices</NavLink>
            <NavLink to="/health">Health</NavLink>
            <button className="logout" onClick={logout}>Log out</button>
          </>
        )}
      </header>
      <main>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/" element={<RequireAuth><DevicesPage /></RequireAuth>} />
          <Route path="/health" element={<RequireAuth><HealthPage /></RequireAuth>} />
        </Routes>
      </main>
    </>
  )
}