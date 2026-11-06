export type Device = {
  id: number
  netbox_id: number
  name: string
  site: string | null
  platform: string | null
  mgmt_ip: string | null
  last_backup_at: string | null
  drift_status: string
}

export type Health = { api: string; database: string; redis: string; mock_mode: boolean }
export type SyncResult = { created: number; updated: number; total: number }

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const r = await fetch(`/api${path}`, init)
  if (!r.ok) {
    const body = await r.json().catch(() => ({}))
    throw new Error(body.detail ?? `HTTP ${r.status}`)
  }
  return r.json()
}

export const api = {
  health: () => request<Health>('/health'),
  devices: () => request<Device[]>('/devices'),
  syncDevices: () => request<SyncResult>('/devices/sync', { method: 'POST' }),
}