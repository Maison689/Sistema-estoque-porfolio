import { apiRequest } from './apiClient'
import {
  type AdjustmentPayload,
  type Movement,
  type MovementPage,
  type MovementPayload,
  type MovementType,
} from '../types/movement'

export type MovementFilters = {
  createdById?: string
  dateFrom?: string
  dateTo?: string
  limit?: number
  offset?: number
  productId?: string
  type?: MovementType | ''
}

export function listMovements(
  token: string,
  filters: MovementFilters = {},
): Promise<MovementPage> {
  const params = new URLSearchParams()
  params.set('limit', String(filters.limit ?? 20))
  params.set('offset', String(filters.offset ?? 0))
  if (filters.createdById) params.set('created_by_id', filters.createdById)
  if (filters.dateFrom) params.set('date_from', filters.dateFrom)
  if (filters.dateTo) params.set('date_to', filters.dateTo)
  if (filters.productId) params.set('product_id', filters.productId)
  if (filters.type) params.set('type', filters.type)
  const query = params.toString()

  return apiRequest<MovementPage>(`/movements?${query}`, { token })
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
