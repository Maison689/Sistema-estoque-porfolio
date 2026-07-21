# Sis Estoque Backend

Base FastAPI, SQLAlchemy e Alembic da API Sis Estoque.

## Comandos

```powershell
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe -m alembic current
```

A API expoe o healthcheck em `http://127.0.0.1:8000/api/v1/health`.

## Autenticacao

Endpoints principais:

- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `POST /api/v1/auth/logout`
- `GET /api/v1/users` para Administrador

## Categorias e produtos

Endpoints principais:

- `GET /api/v1/categories` para perfis autenticados
- `POST /api/v1/categories` para Administrador e Gestor
- `PATCH /api/v1/categories/{id}` para Administrador e Gestor
- `GET /api/v1/products` para perfis autenticados
- `POST /api/v1/products` para Administrador e Gestor
- `PATCH /api/v1/products/{id}` para Administrador e Gestor

Produtos novos criam saldo `0.000` em `inventory_balances`. O cadastro nao
aceita alteracao direta de saldo.

## Fornecedores e vinculos

Endpoints principais:

- `GET /api/v1/suppliers` para perfis autenticados
- `POST /api/v1/suppliers` para Administrador e Gestor
- `PATCH /api/v1/suppliers/{id}` para Administrador e Gestor
- `GET /api/v1/products/{product_id}/suppliers` para perfis autenticados
- `POST /api/v1/products/{product_id}/suppliers` para Administrador e Gestor
- `DELETE /api/v1/products/{product_id}/suppliers/{supplier_id}` para
  Administrador e Gestor

Fornecedores aceitam CPF ou CNPJ valido e unico quando o documento fiscal e
informado. Fornecedores ou produtos inativos nao recebem novos vinculos.

Criar administrador local inicial:

```powershell
$env:ADMIN_INITIAL_EMAIL='admin@empresa.com'
$env:ADMIN_INITIAL_PASSWORD='defina-uma-senha-local'
$env:ADMIN_INITIAL_NAME='Administrador'
.\.venv\Scripts\python.exe -m scripts.create_initial_admin
```
