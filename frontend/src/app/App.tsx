import { useEffect, useMemo, useState } from 'react'
import { AppShell } from '../components/AppShell'
import { AccessDeniedState, LoadingState } from '../components/StateViews'
import { AccessView } from '../features/access/AccessView'
import { DashboardView } from '../features/dashboard/DashboardView'
import { MovementsView } from '../features/movements/MovementsView'
import { ProductsView } from '../features/products/ProductsView'
import { StatesView } from '../features/states/StatesView'
import { SuppliersView } from '../features/suppliers/SuppliersView'
import { UsersView } from '../features/users/UsersView'
import {
  clearStoredToken,
  getCurrentUser,
  getStoredToken,
  login,
  logout,
} from '../services/authService'
import { type CurrentUser } from '../types/auth'
import { type AppRoute } from './routes'

export function App() {
  const [activeRoute, setActiveRoute] = useState<AppRoute>('login')
  const [authError, setAuthError] = useState<string | null>(null)
  const [authStatus, setAuthStatus] = useState<'checking' | 'ready' | 'submitting'>(
    'checking',
  )
  const [token, setToken] = useState<string | null>(() => getStoredToken())
  const [user, setUser] = useState<CurrentUser | null>(null)
  const pageTitle = useMemo(() => getPageTitle(activeRoute), [activeRoute])

  useEffect(() => {
    if (!token) {
      setAuthStatus('ready')
      setActiveRoute('login')
      return
    }

    getCurrentUser(token)
      .then((currentUser) => {
        setUser(currentUser)
        setAuthStatus('ready')
        setActiveRoute(currentUser.role === 'OPERATOR' ? 'products' : 'dashboard')
      })
      .catch(() => {
        clearStoredToken()
        setToken(null)
        setUser(null)
        setAuthStatus('ready')
        setActiveRoute('login')
      })
  }, [token])

  async function handleLogin(email: string, password: string) {
    setAuthError(null)
    setAuthStatus('submitting')
    try {
      const accessToken = await login(email, password)
      setToken(accessToken)
    } catch {
      setAuthError('Credenciais invalidas ou usuario inativo.')
      setAuthStatus('ready')
    }
  }

  async function handleLogout() {
    await logout(token)
    setToken(null)
    setUser(null)
    setActiveRoute('login')
  }

  if (authStatus === 'checking') {
    return <LoadingState />
  }

  return (
    <AppShell
      activeRoute={activeRoute}
      onLogout={handleLogout}
      onRouteChange={setActiveRoute}
      pageTitle={pageTitle}
      user={user}
    >
      {!user && (
        <AccessView
          error={authError}
          isSubmitting={authStatus === 'submitting'}
          onLogin={handleLogin}
        />
      )}
      {user && activeRoute === 'dashboard' && (
        user.role === 'OPERATOR' ? <AccessDeniedState /> : <DashboardView />
      )}
      {user && token && activeRoute === 'products' && <ProductsView token={token} user={user} />}
      {user && token && activeRoute === 'movements' && (
        <MovementsView token={token} user={user} />
      )}
      {user && token && activeRoute === 'suppliers' && (
        <SuppliersView token={token} user={user} />
      )}
      {user && activeRoute === 'users' && (
        user.role === 'ADMIN' && token ? <UsersView token={token} /> : <AccessDeniedState />
      )}
      {user && token && activeRoute === 'login' && <ProductsView token={token} user={user} />}
      {user && activeRoute === 'states' && <StatesView />}
    </AppShell>
  )
}

function getPageTitle(route: AppRoute) {
  const titles: Record<AppRoute, string> = {
    dashboard: 'Dashboard',
    login: 'Acesso',
    movements: 'Movimentacoes',
    products: 'Catalogo de produtos',
    states: 'Estados da interface',
    suppliers: 'Fornecedores',
    users: 'Usuarios',
  }

  return titles[route]
}
