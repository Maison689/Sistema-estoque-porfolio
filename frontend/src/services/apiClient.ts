const defaultBaseUrl = 'http://localhost:8000/api/v1'

export const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? defaultBaseUrl

type ApiRequestOptions = {
  body?: unknown
  method?: 'DELETE' | 'GET' | 'POST' | 'PATCH'
  token?: string | null
}

export async function apiRequest<TResponse>(
  path: string,
  options: ApiRequestOptions = {},
): Promise<TResponse> {
  const headers = new Headers({
    Accept: 'application/json',
  })
  if (options.body !== undefined) {
    headers.set('Content-Type', 'application/json')
  }
  if (options.token) {
    headers.set('Authorization', `Bearer ${options.token}`)
  }

  const response = await fetch(`${apiBaseUrl}${path}`, {
    body: options.body === undefined ? undefined : JSON.stringify(options.body),
    headers,
    method: options.method ?? 'GET',
  })

  if (!response.ok) {
    throw new Error(`API request failed with status ${response.status}`)
  }

  if (response.status === 204) {
    return undefined as TResponse
  }

  return response.json() as Promise<TResponse>
}

export function apiGet<TResponse>(path: string): Promise<TResponse> {
  return apiRequest<TResponse>(path)
}
