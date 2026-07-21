import { type FormEvent, useState } from 'react'

type AccessViewProps = {
  error: string | null
  isSubmitting: boolean
  onLogin: (email: string, password: string) => Promise<void>
}

export function AccessView({ error, isSubmitting, onLogin }: AccessViewProps) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    await onLogin(email, password)
  }

  return (
    <section className="login-layout">
      <form className="login-panel" onSubmit={handleSubmit}>
        <div>
          <p className="eyebrow">Entrada segura</p>
          <h2>Acessar o Sis Estoque</h2>
        </div>

        <label>
          E-mail
          <input
            onChange={(event) => setEmail(event.target.value)}
            placeholder="usuario@empresa.com"
            type="email"
            value={email}
          />
        </label>

        <label>
          Senha
          <input
            onChange={(event) => setPassword(event.target.value)}
            placeholder="Sua senha"
            type="password"
            value={password}
          />
        </label>

        {error ? <p className="form-error">{error}</p> : null}
        <button disabled={isSubmitting} type="submit">
          {isSubmitting ? 'Entrando...' : 'Entrar'}
        </button>
      </form>
    </section>
  )
}
