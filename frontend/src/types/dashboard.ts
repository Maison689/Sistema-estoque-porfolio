import { type Product } from './inventory'
import { type Movement, type MovementType } from './movement'

export type DashboardMetrics = {
  active_products: number
  inactive_products: number
  low_stock_products: number
  total_movements: number
}

export type MovementTypeSummary = {
  count: number
  quantity_delta_total: string
  type: MovementType
}

export type Dashboard = {
  low_stock_products: Product[]
  metrics: DashboardMetrics
  movement_summary: MovementTypeSummary[]
  recent_movements: Movement[]
}
