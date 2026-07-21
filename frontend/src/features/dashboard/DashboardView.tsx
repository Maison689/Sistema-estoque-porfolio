import { DataTable } from '../../components/DataTable'
import { EmptyState } from '../../components/StateViews'
import { MetricCard } from '../../components/MetricCard'
import { dashboardMetrics, lowStockRows } from '../../data/mockData'

export function DashboardView() {
  return (
    <div className="page-stack">
      <section className="metric-grid" aria-label="Indicadores do dashboard">
        {dashboardMetrics.map((metric) => (
          <MetricCard
            key={metric.label}
            label={metric.label}
            tone={metric.tone}
            value={metric.value}
          />
        ))}
      </section>

      <section className="content-grid">
        <div className="panel panel--wide">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Estoque minimo</p>
              <h2>Produtos que precisam de atencao</h2>
            </div>
            <button type="button">Ver todos</button>
          </div>

          <DataTable
            columns={[
              { key: 'product', label: 'Produto' },
              { key: 'sku', label: 'SKU' },
              { key: 'quantity', label: 'Qtd.', align: 'right' },
              { key: 'status', label: 'Status' },
            ]}
            rows={lowStockRows}
          />
        </div>

        <EmptyState />
      </section>
    </div>
  )
}
