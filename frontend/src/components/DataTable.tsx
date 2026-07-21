export type DataTableColumn<TRow> = {
  align?: 'left' | 'right'
  key: keyof TRow
  label: string
}

type DataTableProps<TRow> = {
  columns: DataTableColumn<TRow>[]
  rows: TRow[]
}

export function DataTable<TRow extends Record<string, string | number>>({
  columns,
  rows,
}: DataTableProps<TRow>) {
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            {columns.map((column) => (
              <th className={column.align === 'right' ? 'align-right' : ''} key={String(column.key)}>
                {column.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {columns.map((column) => (
                <td
                  className={column.align === 'right' ? 'align-right' : ''}
                  key={String(column.key)}
                >
                  {row[column.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
