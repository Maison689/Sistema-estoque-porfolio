import { useEffect, useState } from 'react'
import { DataTable } from '../../components/DataTable'
import { ErrorState, LoadingState } from '../../components/StateViews'
import { listUsers } from '../../services/authService'
import { type UserResponse } from '../../types/auth'

type UsersViewProps = {
  token: string
}

export function UsersView({ token }: UsersViewProps) {
  const [users, setUsers] = useState<UserResponse[]>([])
  const [status, setStatus] = useState<'error' | 'loading' | 'ready'>('loading')

  useEffect(() => {
    listUsers(token)
      .then((response) => {
        setUsers(response)
        setStatus('ready')
      })
      .catch(() => setStatus('error'))
  }, [token])

  if (status === 'loading') return <LoadingState />
  if (status === 'error') return <ErrorState />

  return (
    <section className="panel">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Administracao</p>
          <h2>Usuarios</h2>
        </div>
        <button type="button">Novo usuario</button>
      </div>
      <DataTable
        columns={[
          { key: 'name', label: 'Nome' },
          { key: 'email', label: 'E-mail' },
          { key: 'role', label: 'Perfil' },
          { key: 'is_active', label: 'Ativo' },
        ]}
        rows={users.map((user) => ({
          email: user.email,
          is_active: user.is_active ? 'Sim' : 'Nao',
          name: user.name,
          role: user.role,
        }))}
      />
    </section>
  )
}
