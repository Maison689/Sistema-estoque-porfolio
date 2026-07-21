export type ProductUnit = 'UN' | 'CX' | 'KG' | 'G' | 'L' | 'ML' | 'M' | 'CM'

export type Category = {
  description: string | null
  id: number
  is_active: boolean
  name: string
}

export type Product = {
  category_id: number
  category_name: string
  id: number
  is_active: boolean
  is_below_minimum: boolean
  minimum_stock: string
  name: string
  quantity: string
  sku: string
  unit: ProductUnit
}

export type CategoryPayload = {
  description?: string | null
  is_active?: boolean
  name: string
}

export type ProductPayload = {
  category_id: number
  is_active?: boolean
  minimum_stock: string
  name: string
  sku: string
  unit: ProductUnit
}
