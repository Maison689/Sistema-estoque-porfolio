import { type CurrentUser, type LoginResponse, type UserResponse } from '../types/auth'
import { apiRequest } from './apiClient'

const tokenStorageKey = 'sis_estoque_token'

export function getStoredToken() {
  return window.localStorage.getItem(tokenStorageKey)
}

export function storeToken(token: string) {
  window.localStorage.setItem(tokenStorageKey, token)
}

export function clearStoredToken() {
  window.localStorage.removeItem(tokenStorageKey)
}

export async function login(email: string, password: string) {
  const response = await apiRequest<LoginResponse>('/auth/login', {
    body: { email, password },
    method: 'POST',
  })
  storeToken(response.access_token)
  return response.access_token
}

export function getCurrentUser(token: string) {
  return apiRequest<CurrentUser>('/auth/me', { token })
}

export async function logout(token: string | null) {
  if (token) {
    await apiRequest('/auth/logout', { method: 'POST', token })
  }
  clearStoredToken()
}

export function listUsers(token: string) {
  return apiRequest<UserResponse[]>('/users', { token })
}
