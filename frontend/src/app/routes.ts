export type AppRoute =
  | 'dashboard'
  | 'products'
  | 'movements'
  | 'suppliers'
  | 'users'
  | 'login'
  | 'states'

export type NavigationItem = {
  id: AppRoute
  label: string
  icon: string
}

export const navigationItems: NavigationItem[] = [
  { id: 'dashboard', label: 'Dashboard', icon: 'D' },
  { id: 'products', label: 'Produtos', icon: 'P' },
  { id: 'movements', label: 'Movimentacoes', icon: 'M' },
  { id: 'suppliers', label: 'Fornecedores', icon: 'F' },
  { id: 'users', label: 'Usuarios', icon: 'U' },
  { id: 'login', label: 'Login', icon: 'L' },
  { id: 'states', label: 'Estados', icon: 'S' },
]
