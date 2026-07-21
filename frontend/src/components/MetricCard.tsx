type MetricCardProps = {
  label: string
  tone?: 'default' | 'danger' | 'success' | 'warning'
  value: string
}

export function MetricCard({ label, tone = 'default', value }: MetricCardProps) {
  return (
    <article className={`metric-card metric-card--${tone}`}>
      <span>{label}</span>
      <strong>{value}</strong>
    </article>
  )
}
