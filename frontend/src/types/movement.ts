export type MovementType = 'ENTRY' | 'EXIT' | 'ADJUSTMENT'

export type Movement = {
  balance_after: string
  balance_before: string
  created_at: string
  created_by_id: number
  created_by_name: string
  id: number
  note: string | null
  product_id: number
  product_name: string
  product_sku: string
  quantity_delta: string
  reason: string | null
  type: MovementType
}

export type MovementPage = {
  items: Movement[]
  limit: number
  offset: number
  total: number
}

export type MovementPayload = {
  note?: string | null
  product_id: number
  quantity: string
}

export type AdjustmentPayload = {
  note?: string | null
  product_id: number
  quantity_delta: string
  reason: string
}
