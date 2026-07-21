export type Supplier = {
  email: string | null
  id: number
  is_active: boolean
  name: string
  phone: string | null
  products_count: number
  tax_id: string | null
}

export type SupplierPayload = {
  email?: string | null
  is_active?: boolean
  name: string
  phone?: string | null
  tax_id?: string | null
}

export type ProductSupplierLink = {
  product_id: number
  supplier_email: string | null
  supplier_id: number
  supplier_name: string
  supplier_phone: string | null
  supplier_tax_id: string | null
}
