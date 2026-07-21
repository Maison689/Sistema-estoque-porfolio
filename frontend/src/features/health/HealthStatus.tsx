import { useEffect, useState } from 'react'
import { getHealth } from '../../services/healthService'

type HealthState =
  | { status: 'loading'; message: string }
  | { status: 'ready'; message: string }
  | { status: 'offline'; message: string }

export function HealthStatus() {
  const [health, setHealth] = useState<HealthState>({
    status: 'loading',
    message: 'Verificando API',
  })

  useEffect(() => {
    let isCurrent = true

    getHealth()
      .then((response) => {
        if (!isCurrent) return

        setHealth({
          status: 'ready',
          message: response.status === 'ok' ? 'API online' : 'API respondeu',
        })
      })
      .catch(() => {
        if (!isCurrent) return

        setHealth({
          status: 'offline',
          message: 'API offline',
        })
      })

    return () => {
      isCurrent = false
    }
  }, [])

  return (
    <div className={`health-badge health-badge--${health.status}`} role="status">
      <span aria-hidden="true" />
      {health.message}
    </div>
  )
}
