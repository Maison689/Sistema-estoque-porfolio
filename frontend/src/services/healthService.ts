import { apiGet } from './apiClient'

export type HealthResponse = {
  status: 'ok'
  service: string
}

export function getHealth() {
  return apiGet<HealthResponse>('/health')
}
