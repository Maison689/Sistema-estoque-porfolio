import { type AppRoute, navigationItems } from '../app/routes'
import { type CurrentUser } from '../types/auth'

type SidebarProps = {
  activeRoute: AppRoute
  onRouteChange: (route: AppRoute) => void
  user: CurrentUser | null
}

export function Sidebar({ activeRoute, onRouteChange, user }: SidebarProps) {
  const visibleItems = navigationItems.filter((item) => {
    if (user === null) return item.id === 'login'
    if (item.id === 'users') return user?.role === 'ADMIN'
    if (item.id === 'dashboard') return user?.role !== 'OPERATOR'
    if (item.id === 'login') return false
    return true
  })

  return (
    <aside className="sidebar">
      <div className="brand-block">
        <strong>Sis Estoque</strong>
        <span>Stock Management</span>
      </div>

      <nav aria-label="Navegacao principal" className="nav-list">
        {visibleItems.map((item) => (
          <button
            aria-current={activeRoute === item.id ? 'page' : undefined}
            className={activeRoute === item.id ? 'nav-link is-active' : 'nav-link'}
            key={item.id}
            onClick={() => onRouteChange(item.id)}
            type="button"
          >
            <span aria-hidden="true" className="nav-icon">
              {item.icon}
            </span>
            {item.label}
          </button>
        ))}
      </nav>
    </aside>
  )
}
