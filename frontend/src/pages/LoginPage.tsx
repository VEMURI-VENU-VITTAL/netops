import { useState } from 'react'
import type { FormEvent } from 'react'
import { useMutation } from '@tanstack/react-query'
import { useNavigate } from 'react-router'
import { api, auth } from '../api'

export default function LoginPage() {
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  const login = useMutation({
    mutationFn: () => api.login(username, password),
    onSuccess: (data) => {
      auth.set(data.access_token)
      navigate('/')
    },
  })

  const submit = (e: FormEvent) => {
    e.preventDefault()
    login.mutate()
  }

  return (
    <form className="login" onSubmit={submit}>
      <h1>Sign in</h1>
      <input placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
      <input type="password" placeholder="Password" value={password}
             onChange={(e) => setPassword(e.target.value)} />
      <button type="submit" disabled={login.isPending}>
        {login.isPending ? 'Signing in...' : 'Sign in'}
      </button>
      {login.isError && <p className="error">{login.error.message}</p>}
    </form>
  )
}