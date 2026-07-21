import { apiRequest } from './apiClient'
import {
  type AdjustmentPayload,
  type Movement,
  type MovementPayload,
  type MovementType,
} from '../types/movement'

export type MovementFilters = {
  productId?: string
  type?: MovementType | ''
}

export function listMovements(
  token: string,
  filters: MovementFilters = {},
): Promise<Movement[]> {
  const params = new URLSearchParams()
  if (filters.productId) params.set('product_id', filters.productId)
  if (filters.type) params.set('type', filters.type)
  const query = params.toString()

  return apiRequest<Movement[]>(`/movements${query ? `?${query}` : ''}`, { token })
}

export function createEntry(
  token: string,
  payload: MovementPayload,
): Promise<Movement> {
  return apiRequest<Movement>('/movements/entries', {
    body: payload,
    method: 'POST',
    token,
  })
}

export function createExit(
  token: string,
  payload: MovementPayload,
): Promise<Movement> {
  return apiRequest<Movement>('/movements/exits', {
    body: payload,
    method: 'POST',
    token,
  })
}

export function createAdjustment(
  token: string,
  payload: AdjustmentPayload,
): Promise<Movement> {
  return apiRequest<Movement>('/movements/adjustments', {
    body: payload,
    method: 'POST',
    token,
  })
}
