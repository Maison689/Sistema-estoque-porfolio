import { DataTable } from '../../components/DataTable'
import { movementRows } from '../../data/mockData'

export function MovementsView() {
  return (
    <div className="page-stack">
      <section className="action-row" aria-label="Registrar movimentacao">
        <button type="button">Registrar entrada</button>
        <button type="button">Registrar saida</button>
        <button type="button">Registrar ajuste</button>
      </section>

      <section className="toolbar-panel">
        <label>
          Tipo
          <select>
            <option>Todos</option>
            <option>Entrada</option>
            <option>Saida</option>
            <option>Ajuste</option>
          </select>
        </label>
        <label>
          Periodo inicial
          <input type="date" />
        </label>
        <label>
          Periodo final
          <input type="date" />
        </label>
      </section>

      <section className="panel">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Historico</p>
            <h2>Movimentacoes recentes</h2>
          </div>
        </div>

        <DataTable
          columns={[
            { key: 'date', label: 'Data/Hora' },
            { key: 'type', label: 'Tipo' },
            { key: 'product', label: 'Produto' },
            { key: 'quantity', label: 'Qtd.', align: 'right' },
            { key: 'user', label: 'Responsavel' },
          ]}
          rows={movementRows}
        />
      </section>
    </div>
  )
}
