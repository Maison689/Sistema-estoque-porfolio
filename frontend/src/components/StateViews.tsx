type StateViewProps = {
  actionLabel?: string
  message: string
  title: string
  tone?: 'neutral' | 'danger' | 'warning'
}

function StateView({ actionLabel, message, title, tone = 'neutral' }: StateViewProps) {
  return (
    <section className={`state-panel state-panel--${tone}`}>
      <strong>{title}</strong>
      <p>{message}</p>
      {actionLabel ? <button type="button">{actionLabel}</button> : null}
    </section>
  )
}

export function LoadingState() {
  return (
    <section className="state-panel">
      <div aria-label="Carregando" className="loading-bar" role="status" />
      <strong>Carregando dados</strong>
      <p>A interface esta aguardando a resposta da API.</p>
    </section>
  )
}

export function EmptyState() {
  return (
    <StateView
      actionLabel="Criar primeiro registro"
      message="Quando a API retornar uma lista vazia, esta area orienta o proximo passo."
      title="Nenhum registro encontrado"
    />
  )
}

export function ErrorState() {
  return (
    <StateView
      actionLabel="Tentar novamente"
      message="Falhas de consulta aparecem com uma acao clara, sem expor detalhes internos."
      title="Nao foi possivel carregar"
      tone="danger"
    />
  )
}

export function AccessDeniedState() {
  return (
    <StateView
      message="Este estado sera usado quando o perfil autenticado nao tiver permissao."
      title="Acesso negado"
      tone="warning"
    />
  )
}
