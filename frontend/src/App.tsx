import { NavLink, Route, Routes } from 'react-router'
import DevicesPage from './pages/DevicesPage'
import HealthPage from './pages/HealthPage'

export default function App() {
  return (
    <>
      <header>
        <strong>NetOps Portal</strong>
        <NavLink to="/" end>Devices</NavLink>
        <NavLink to="/health">Health</NavLink>
      </header>
      <main>
        <Routes>
          <Route path="/" element={<DevicesPage />} />
          <Route path="/health" element={<HealthPage />} />
        </Routes>
      </main>
    </>
  )
}