import { useCallback, useEffect, useMemo, useState } from 'react'
import { MetricCard } from '../../components/MetricCard'
import { getDashboard } from '../../services/dashboardService'
import { type Dashboard } from '../../types/dashboard'
import { type MovementType } from '../../types/movement'

type DashboardViewProps = {
  token: string
}

export function DashboardView({ token }: DashboardViewProps) {
  const [dashboard, setDashboard] = useState<Dashboard | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const refreshDashboard = useCallback(async () => {
    setIsLoading(true)
    setError(null)
    try {
      setDashboard(await getDashboard(token))
    } catch {
      setError('Nao foi possivel carregar o dashboard.')
    } finally {
      setIsLoading(false)
    }
  }, [token])

  useEffect(() => {
    refreshDashboard()
  }, [refreshDashboard])

  const metrics = useMemo(() => {
    if (!dashboard) return []

    return [
      {
        label: 'Produtos ativos',
        tone: 'default',
        value: String(dashboard.metrics.active_products),
      },
      {
        label: 'Abaixo do minimo',
        tone: dashboard.metrics.low_stock_products > 0 ? 'warning' : 'success',
        value: String(dashboard.metrics.low_stock_products),
      },
      {
        label: 'Movimentacoes',
        tone: 'default',
        value: String(dashboard.metrics.total_movements),
      },
      {
        label: 'Produtos inativos',
        tone: 'default',
        value: String(dashboard.metrics.inactive_products),
      },
    ] as const
  }, [dashboard])

  if (isLoading) {
    return (
      <div className="state-panel">
        <strong>Carregando dados</strong>
        <div className="loading-bar" />
      </div>
    )
  }

  if (error) {
    return (
      <div className="state-panel state-panel--danger">
        <strong>{error}</strong>
        <button onClick={refreshDashboard} type="button">
          Atualizar
        </button>
      </div>
    )
  }

  if (!dashboard) {
    return (
      <div className="state-panel">
        <strong>Nenhum registro encontrado</strong>
      </div>
    )
  }

  return (
    <div className="page-stack">
      <section className="metric-grid" aria-label="Indicadores do dashboard">
        {metrics.map((metric) => (
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
          </div>

          {dashboard.low_stock_products.length === 0 ? (
            <div className="state-panel">
              <strong>Nenhum registro encontrado</strong>
              <p>Todos os produtos ativos estao dentro do estoque minimo.</p>
            </div>
          ) : (
            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>Produto</th>
                    <th>SKU</th>
                    <th className="align-right">Saldo</th>
                    <th className="align-right">Minimo</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {dashboard.low_stock_products.map((product) => (
                    <tr key={product.id}>
                      <td>{product.name}</td>
                      <td>{product.sku}</td>
                      <td className="align-right">{product.quantity}</td>
                      <td className="align-right">{product.minimum_stock}</td>
                      <td>
                        <span className="status-pill status-pill--warning">
                          Abaixo do minimo
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        <div className="panel">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Movimentacoes</p>
              <h2>Resumo por tipo</h2>
            </div>
          </div>
          <div className="summary-list">
            {dashboard.movement_summary.map((summary) => (
              <div className="summary-row" key={summary.type}>
                <span>{movementTypeLabel(summary.type)}</span>
                <strong>{summary.count}</strong>
                <small>{summary.quantity_delta_total}</small>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="panel">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Atividade</p>
            <h2>Movimentacoes recentes</h2>
          </div>
          <button onClick={refreshDashboard} type="button">
            Atualizar
          </button>
        </div>
        {dashboard.recent_movements.length === 0 ? (
          <div className="state-panel">
            <strong>Nenhum registro encontrado</strong>
            <p>As movimentacoes recentes aparecerao aqui.</p>
          </div>
        ) : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Data/Hora</th>
                  <th>Tipo</th>
                  <th>Produto</th>
                  <th className="align-right">Variacao</th>
                  <th className="align-right">Saldo final</th>
                  <th>Responsavel</th>
                </tr>
              </thead>
              <tbody>
                {dashboard.recent_movements.map((movement) => (
                  <tr key={movement.id}>
                    <td>{new Date(movement.created_at).toLocaleString('pt-BR')}</td>
                    <td>{movementTypeLabel(movement.type)}</td>
                    <td>{movement.product_name}</td>
                    <td className="align-right">{movement.quantity_delta}</td>
                    <td className="align-right">{movement.balance_after}</td>
                    <td>{movement.created_by_name}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  )
}

function movementTypeLabel(type: MovementType) {
  const labels: Record<MovementType, string> = {
    ADJUSTMENT: 'Ajuste',
    ENTRY: 'Entrada',
    EXIT: 'Saida',
  }

  return labels[type]
}
