import { apiRequest } from './apiClient'
import {
  type Category,
  type CategoryPayload,
  type Product,
  type ProductPayload,
} from '../types/inventory'

export type ProductFilters = {
  categoryId?: string
  search?: string
  stockStatus?: string
}

export function listCategories(token: string): Promise<Category[]> {
  return apiRequest<Category[]>('/categories', { token })
}

export function createCategory(
  token: string,
  payload: CategoryPayload,
): Promise<Category> {
  return apiRequest<Category>('/categories', {
    body: payload,
    method: 'POST',
    token,
  })
}

export function updateCategory(
  token: string,
  categoryId: number,
  payload: Partial<CategoryPayload>,
): Promise<Category> {
  return apiRequest<Category>(`/categories/${categoryId}`, {
    body: payload,
    method: 'PATCH',
    token,
  })
}

export function listProducts(
  token: string,
  filters: ProductFilters = {},
): Promise<Product[]> {
  const params = new URLSearchParams()
  if (filters.search) params.set('search', filters.search)
  if (filters.categoryId) params.set('category_id', filters.categoryId)
  if (filters.stockStatus) params.set('stock_status', filters.stockStatus)
  const query = params.toString()

  return apiRequest<Product[]>(`/products${query ? `?${query}` : ''}`, { token })
}

export function createProduct(
  token: string,
  payload: ProductPayload,
): Promise<Product> {
  return apiRequest<Product>('/products', {
    body: payload,
    method: 'POST',
    token,
  })
}

export function updateProduct(
  token: string,
  productId: number,
  payload: Partial<ProductPayload>,
): Promise<Product> {
  return apiRequest<Product>(`/products/${productId}`, {
    body: payload,
    method: 'PATCH',
    token,
  })
}
