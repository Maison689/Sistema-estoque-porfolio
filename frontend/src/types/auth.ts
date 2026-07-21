export type UserRole = 'ADMIN' | 'MANAGER' | 'OPERATOR'

export type CurrentUser = {
  id: number
  name: string
  email: string
  role: UserRole
  is_active: boolean
}

export type LoginResponse = {
  access_token: string
  token_type: 'bearer'
}

export type UserResponse = CurrentUser
