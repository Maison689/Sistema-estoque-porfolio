import { useCallback, useEffect, useMemo, useState } from 'react'
import { listProducts } from '../../services/inventoryService'
import {
  createAdjustment,
  createEntry,
  createExit,
  listMovements,
  type MovementFilters,
} from '../../services/movementService'
import { type CurrentUser } from '../../types/auth'
import { type Product } from '../../types/inventory'
import { type Movement, type MovementType } from '../../types/movement'

type MovementsViewProps = {
  token: string
  user: CurrentUser
}

type MovementFormState = {
  note: string
  productId: string
  quantity: string
  reason: string
  type: MovementType
}

const emptyForm: MovementFormState = {
  note: '',
  productId: '',
  quantity: '1.000',
  reason: '',
  type: 'ENTRY',
}

export function MovementsView({ token, user }: MovementsViewProps) {
  const canAdjust = user.role === 'ADMIN' || user.role === 'MANAGER'
  const [products, setProducts] = useState<Product[]>([])
  const [movements, setMovements] = useState<Movement[]>([])
  const [filters, setFilters] = useState<MovementFilters>({})
  const [form, setForm] = useState<MovementFormState>(emptyForm)
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const activeProducts = useMemo(
    () => products.filter((product) => product.is_active),
    [products],
  )
  const availableTypes: MovementType[] = canAdjust
    ? ['ENTRY', 'EXIT', 'ADJUSTMENT']
    : ['ENTRY', 'EXIT']

  const refreshMovements = useCallback(
    async (nextFilters: MovementFilters = filters) => {
      setIsLoading(true)
      setError(null)
      try {
        const [productResult, movementResult] = await Promise.all([
          listProducts(token),
          listMovements(token, nextFilters),
        ])
        setProducts(productResult)
        setMovements(movementResult)
        if (!form.productId && productResult.length > 0) {
          setForm((current) => ({ ...current, productId: String(productResult[0].id) }))
        }
      } catch {
        setError('Nao foi possivel carregar movimentacoes.')
      } finally {
        setIsLoading(false)
      }
    },
    [filters, form.productId, token],
  )

  useEffect(() => {
    refreshMovements()
  }, [refreshMovements])

  async function handleFilterChange(nextFilters: MovementFilters) {
    setFilters(nextFilters)
    await refreshMovements(nextFilters)
  }

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!form.productId) return
    if (form.type === 'ADJUSTMENT' && !canAdjust) return
    setIsSaving(true)
    setError(null)

    try {
      const common = {
        note: form.note.trim() || null,
        product_id: Number(form.productId),
      }
      if (form.type === 'ENTRY') {
        await createEntry(token, { ...common, quantity: form.quantity })
      } else if (form.type === 'EXIT') {
        await createExit(token, { ...common, quantity: form.quantity })
      } else {
        await createAdjustment(token, {
          ...common,
          quantity_delta: form.quantity,
          reason: form.reason,
        })
      }
      setForm({ ...emptyForm, productId: form.productId, type: form.type })
      await refreshMovements()
    } catch {
      setError('Nao foi possivel registrar a movimentacao.')
    } finally {
      setIsSaving(false)
    }
  }

  return (
    <div className="page-stack">
      <form className="panel form-panel" onSubmit={handleSubmit}>
        <div className="section-heading">
          <div>
            <p className="eyebrow">Movimentacao</p>
            <h2>Registrar movimentacao de estoque</h2>
          </div>
        </div>
        <div className="form-grid form-grid--two">
          <label>
            Produto
            <select
              onChange={(event) => setForm({ ...form, productId: event.target.value })}
              required
              value={form.productId}
            >
              <option value="">Selecione</option>
              {activeProducts.map((product) => (
                <option key={product.id} value={product.id}>
                  {product.name} - saldo {product.quantity} {product.unit}
                </option>
              ))}
            </select>
          </label>
          <label>
            Tipo
            <select
              onChange={(event) =>
                setForm({ ...form, type: event.target.value as MovementType })
              }
              value={form.type}
            >
              {availableTypes.map((type) => (
                <option key={type} value={type}>
                  {movementTypeLabel(type)}
                </option>
              ))}
            </select>
          </label>
          <label>
            Quantidade
            <input
              min={form.type === 'ADJUSTMENT' ? undefined : '0.001'}
              onChange={(event) => setForm({ ...form, quantity: event.target.value })}
              required
              step="0.001"
              type="number"
              value={form.quantity}
            />
          </label>
          {form.type === 'ADJUSTMENT' && (
            <label>
              Justificativa
              <input
                onChange={(event) => setForm({ ...form, reason: event.target.value })}
                required
                value={form.reason}
              />
            </label>
          )}
          <label>
            Observacao
            <input
              onChange={(event) => setForm({ ...form, note: event.target.value })}
              value={form.note}
            />
          </label>
          <div className="action-row action-row--end">
            <button disabled={isSaving || activeProducts.length === 0} type="submit">
              Registrar {movementTypeLabel(form.type).toLowerCase()}
            </button>
          </div>
        </div>
      </form>

      <section className="toolbar-panel">
        <label>
          Produto
          <select
            onChange={(event) =>
              handleFilterChange({ ...filters, productId: event.target.value })
            }
            value={filters.productId ?? ''}
          >
            <option value="">Todos</option>
            {products.map((product) => (
              <option key={product.id} value={product.id}>
                {product.name}
              </option>
            ))}
          </select>
        </label>
        <label>
          Tipo
          <select
            onChange={(event) =>
              handleFilterChange({
                ...filters,
                type: event.target.value as MovementType | '',
              })
            }
            value={filters.type ?? ''}
          >
            <option value="">Todos</option>
            <option value="ENTRY">Entrada</option>
            <option value="EXIT">Saida</option>
            <option value="ADJUSTMENT">Ajuste</option>
          </select>
        </label>
        <button disabled={isLoading} onClick={() => refreshMovements()} type="button">
          Atualizar
        </button>
      </section>

      {error && <p className="form-error">{error}</p>}

      <section className="panel">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Historico</p>
            <h2>Movimentacoes recentes</h2>
          </div>
        </div>
        {isLoading ? (
          <div className="state-panel">
            <strong>Carregando dados</strong>
            <div className="loading-bar" />
          </div>
        ) : movements.length === 0 ? (
          <div className="state-panel">
            <strong>Nenhum registro encontrado</strong>
            <p>Registre entradas, saidas ou ajustes para formar o historico.</p>
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
                  <th className="align-right">Saldo anterior</th>
                  <th className="align-right">Saldo final</th>
                  <th>Responsavel</th>
                </tr>
              </thead>
              <tbody>
                {movements.map((movement) => (
                  <tr key={movement.id}>
                    <td>{new Date(movement.created_at).toLocaleString('pt-BR')}</td>
                    <td>{movementTypeLabel(movement.type)}</td>
                    <td>{movement.product_name}</td>
                    <td className="align-right">{movement.quantity_delta}</td>
                    <td className="align-right">{movement.balance_before}</td>
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
