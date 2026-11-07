const TOKEN_KEY = 'netops_token'

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

export const auth = {
  get: () => localStorage.getItem(TOKEN_KEY),
  set: (token: string) => localStorage.setItem(TOKEN_KEY, token),
  clear: () => localStorage.removeItem(TOKEN_KEY),
}

export type Health = { api: string; database: string; redis: string; mock_mode: boolean }
export type SyncResult = { created: number; updated: number; total: number }

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const headers = new Headers(init?.headers)
  const token = auth.get()
  if (token) headers.set('Authorization', `Bearer ${token}`)

  const r = await fetch(`/api${path}`, { ...init, headers })
  if (r.status === 401 && token) {
    auth.clear()
    window.location.assign('/login')
  }
  if (!r.ok) {
    const body = await r.json().catch(() => ({}))
    throw new Error(body.detail ?? `HTTP ${r.status}`)
  }
  return r.json()
}


export const api = {
  login: (username: string, password: string) =>
    request<{ access_token: string }>('/auth/login', {
      method: 'POST',
      body: new URLSearchParams({ username, password }),
    }),
  health: () => request<Health>('/health'),
  devices: () => request<Device[]>('/devices'),
  syncDevices: () => request<SyncResult>('/devices/sync', { method: 'POST' }),
}