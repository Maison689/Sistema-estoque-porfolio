import {
  AccessDeniedState,
  EmptyState,
  ErrorState,
  LoadingState,
} from '../../components/StateViews'

export function StatesView() {
  return (
    <div className="states-grid">
      <LoadingState />
      <EmptyState />
      <ErrorState />
      <AccessDeniedState />
    </div>
  )
}
