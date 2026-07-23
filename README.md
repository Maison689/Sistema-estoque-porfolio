# Sis Estoque

Sistema web de gerenciamento de estoque para portfolio, construido com
Specification-Driven Development.

## Stack oficial

- Frontend: React 19, TypeScript e Vite
- Backend: Python 3.13, FastAPI e SQLAlchemy
- Banco de dados: PostgreSQL 17
- Deploy: Docker somente na fase de deploy

## Estado atual

A Meta 1 esta aprovada. A Meta 2 preparou o ambiente local e o repositorio. A
Meta 3 criou a fundacao tecnica de frontend, backend e banco local. A Meta 4
criou a experiencia-base navegavel. A Meta 5 adicionou autenticacao,
autorizacao e administracao inicial de usuarios. A Meta 6 entregou categorias,
produtos e saldo inicial zero com API real e tela integrada. A Meta 7 entregou
fornecedores e vinculos com produtos. A Meta 8 entregou movimentacoes de
estoque com entrada, saida, ajuste e consistencia transacional de saldo. A Meta
9 conectou dashboard gerencial, historico paginado/filtravel e destaque de
produtos abaixo do minimo aos dados oficiais.

## Pre-requisitos locais

- Git
- Node.js e npm
- Python 3.13
- PostgreSQL 17

No Windows, se `npm` for bloqueado pela politica de execucao do PowerShell, use
`npm.cmd`.

Nesta maquina, o PostgreSQL 17 foi instalado em `D:\PostgreSQL17` e configurado
na porta `5433`, porque ja existe uma instalacao PostgreSQL 18 usando a porta
`5432`.

## Estrutura prevista

```text
frontend/   # Aplicacao React
backend/    # API FastAPI
docs/       # Especificacao e plano de execucao
```

## Configuracao local

1. Copie `.env.example` para `.env` quando a implementacao iniciar.
2. Ajuste os valores locais sem versionar segredos reais.
3. Use PostgreSQL 17 na porta `5433` para o ambiente local deste projeto.

## Comandos

Frontend:

```powershell
cd frontend
npm.cmd install
npm.cmd run dev
npm.cmd run lint
npm.cmd run test
npm.cmd run build
```

Backend:

```powershell
cd backend
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe -m alembic current
```

Criar administrador local inicial:

```powershell
$env:ADMIN_INITIAL_EMAIL='admin@empresa.com'
$env:ADMIN_INITIAL_PASSWORD='defina-uma-senha-local'
$env:ADMIN_INITIAL_NAME='Administrador'
.\.venv\Scripts\python.exe -m scripts.create_initial_admin
```

## Proximo passo

Apresentar e aprovar o plano da Meta 10.
