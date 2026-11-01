import { useEffect, useState } from 'react'

type Health = { api: string; database: string; redis: string; mock_mode: boolean }

export default function App() {
  const [health, setHealth] = useState<Health | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetch('/api/health')
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`)
        return r.json()
      })
      .then(setHealth)
      .catch((e) => setError(String(e)))
  }, [])

  return (
    <main style={{ fontFamily: 'system-ui', padding: 32 }}>
      <h1>NetOps Portal</h1>
      {error && <p style={{ color: 'crimson' }}>Error: {error}</p>}
      {!health && !error && <p>Checking backend...</p>}
      {health && (
        <ul>
          <li>API: {health.api}</li>
          <li>Database: {health.database}</li>
          <li>Redis: {health.redis}</li>
          <li>Mock mode: {health.mock_mode ? 'on' : 'off'}</li>
        </ul>
      )}
    </main>
  )
}