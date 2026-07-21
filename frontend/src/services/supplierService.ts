import { apiRequest } from './apiClient'
import {
  type ProductSupplierLink,
  type Supplier,
  type SupplierPayload,
} from '../types/supplier'

export type SupplierFilters = {
  isActive?: string
  search?: string
}

export function listSuppliers(
  token: string,
  filters: SupplierFilters = {},
): Promise<Supplier[]> {
  const params = new URLSearchParams()
  if (filters.search) params.set('search', filters.search)
  if (filters.isActive) params.set('is_active', filters.isActive)
  const query = params.toString()

  return apiRequest<Supplier[]>(`/suppliers${query ? `?${query}` : ''}`, { token })
}

export function createSupplier(
  token: string,
  payload: SupplierPayload,
): Promise<Supplier> {
  return apiRequest<Supplier>('/suppliers', {
    body: payload,
    method: 'POST',
    token,
  })
}

export function updateSupplier(
  token: string,
  supplierId: number,
  payload: Partial<SupplierPayload>,
): Promise<Supplier> {
  return apiRequest<Supplier>(`/suppliers/${supplierId}`, {
    body: payload,
    method: 'PATCH',
    token,
  })
}

export function listProductSuppliers(
  token: string,
  productId: number,
): Promise<ProductSupplierLink[]> {
  return apiRequest<ProductSupplierLink[]>(`/products/${productId}/suppliers`, {
    token,
  })
}

export function createProductSupplier(
  token: string,
  productId: number,
  supplierId: number,
): Promise<ProductSupplierLink> {
  return apiRequest<ProductSupplierLink>(`/products/${productId}/suppliers`, {
    body: { supplier_id: supplierId },
    method: 'POST',
    token,
  })
}

export function deleteProductSupplier(
  token: string,
  productId: number,
  supplierId: number,
): Promise<void> {
  return apiRequest<void>(`/products/${productId}/suppliers/${supplierId}`, {
    method: 'DELETE',
    token,
  })
}
