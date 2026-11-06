import { useQuery } from '@tanstack/react-query'
import { api } from '../api'

export default function HealthPage() {
  const health = useQuery({ queryKey: ['health'], queryFn: api.health })

  return (
    <>
      <h1>System health</h1>
      {health.isLoading && <p>Checking...</p>}
      {health.isError && <p className="error">{health.error.message}</p>}
      {health.data && (
        <ul>
          <li>API: {health.data.api}</li>
          <li>Database: {health.data.database}</li>
          <li>Redis: {health.data.redis}</li>
          <li>Mock mode: {health.data.mock_mode ? 'on' : 'off'}</li>
        </ul>
      )}
    </>
  )
}