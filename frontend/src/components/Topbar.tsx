import { type ReactNode } from 'react'
import { type CurrentUser } from '../types/auth'

type TopbarProps = {
  children: ReactNode
  onLogout: () => void
  pageTitle: string
  user: CurrentUser | null
}

export function Topbar({ children, onLogout, pageTitle, user }: TopbarProps) {
  return (
    <header className="topbar">
      <div>
        <p className="eyebrow">Sis Estoque</p>
        <h1>{pageTitle}</h1>
      </div>

      <div className="topbar-actions">
        <label className="search-field">
          <span>Buscar</span>
          <input placeholder="Produto, SKU ou fornecedor" type="search" />
        </label>
        {children}
        {user ? (
          <div className="user-chip">
            <span>{user.name}</span>
            <strong>{user.role}</strong>
            <button onClick={onLogout} type="button">
              Sair
            </button>
          </div>
        ) : null}
      </div>
    </header>
  )
}
