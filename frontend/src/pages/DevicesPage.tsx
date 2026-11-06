import { useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { api } from '../api'

const badgeClass: Record<string, string> = { in_sync: 'ok', drift: 'drift' }

export default function DevicesPage() {
  const queryClient = useQueryClient()
  const [search, setSearch] = useState('')

  const devices = useQuery({ queryKey: ['devices'], queryFn: api.devices })
  const sync = useMutation({
    mutationFn: api.syncDevices,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['devices'] }),
  })

  const term = search.toLowerCase()
  const rows = (devices.data ?? []).filter((d) =>
    [d.name, d.site, d.mgmt_ip, d.platform].some((v) => v?.toLowerCase().includes(term)),
  )

  return (
    <>
      <h1>Devices</h1>
      <div className="toolbar">
        <input
          placeholder="Search name, site, IP..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <button onClick={() => sync.mutate()} disabled={sync.isPending}>
          {sync.isPending ? 'Syncing...' : 'Sync from NetBox'}
        </button>
      </div>

      {sync.isSuccess && (
        <p className="note">Synced: {sync.data.created} new, {sync.data.updated} updated.</p>
      )}
      {sync.isError && <p className="error">{sync.error.message}</p>}
      {devices.isLoading && <p>Loading...</p>}
      {devices.isError && <p className="error">{devices.error.message}</p>}

      {devices.data && (
        <table>
          <thead>
            <tr>
              <th>Name</th><th>Site</th><th>Platform</th>
              <th>Mgmt IP</th><th>Last backup</th><th>Drift</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((d) => (
              <tr key={d.id}>
                <td>{d.name}</td>
                <td>{d.site ?? '-'}</td>
                <td>{d.platform ?? '-'}</td>
                <td>{d.mgmt_ip ?? '-'}</td>
                <td>{d.last_backup_at ? new Date(d.last_backup_at).toLocaleString() : 'Never'}</td>
                <td>
                  <span className={`badge ${badgeClass[d.drift_status] ?? 'unknown'}`}>
                    {d.drift_status}
                  </span>
                </td>
              </tr>
            ))}
            {rows.length === 0 && (
              <tr>
                <td colSpan={6} className="note">No devices. Click "Sync from NetBox".</td>
              </tr>
            )}
          </tbody>
        </table>
      )}
    </>
  )
}