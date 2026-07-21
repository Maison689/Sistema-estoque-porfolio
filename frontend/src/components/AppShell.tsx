import { type ReactNode } from 'react'
import { HealthStatus } from '../features/health/HealthStatus'
import { type AppRoute } from '../app/routes'
import { type CurrentUser } from '../types/auth'
import { Sidebar } from './Sidebar'
import { Topbar } from './Topbar'

type AppShellProps = {
  activeRoute: AppRoute
  children: ReactNode
  onRouteChange: (route: AppRoute) => void
  onLogout: () => void
  pageTitle: string
  user: CurrentUser | null
}

export function AppShell({
  activeRoute,
  children,
  onRouteChange,
  onLogout,
  pageTitle,
  user,
}: AppShellProps) {
  return (
    <div className="app-shell">
      <Sidebar activeRoute={activeRoute} onRouteChange={onRouteChange} user={user} />
      <div className="workspace">
        <Topbar onLogout={onLogout} pageTitle={pageTitle} user={user}>
          <HealthStatus />
        </Topbar>
        <main className="main-content">{children}</main>
      </div>
    </div>
  )
}
