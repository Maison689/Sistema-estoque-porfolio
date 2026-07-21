# Sis Estoque Frontend

Base React 19, TypeScript e Vite da aplicacao Sis Estoque.

## Experiencia-base

A interface possui telas-base navegaveis para dashboard, produtos,
movimentacoes, fornecedores, login e estados de interface. O catalogo de
produtos e categorias usa a API real. As demais telas ainda usam dados
simulados separados em `src/data/mockData.ts`.

## Autenticacao

O login usa `POST /api/v1/auth/login`, armazena o token no `localStorage` e
consulta `GET /api/v1/auth/me` para definir perfil e navegacao.

## Catalogo

A tela de produtos consulta `GET /api/v1/categories` e `GET /api/v1/products`.
Administrador e Gestor podem criar e alterar categorias/produtos. Operador
consulta o catalogo sem botoes de manutencao.

## Fornecedores

A tela de fornecedores consulta `GET /api/v1/suppliers` e os vinculos em
`GET /api/v1/products/{product_id}/suppliers`. Administrador e Gestor podem
manter fornecedores e vinculos. Operador consulta sem botoes de manutencao.

## Comandos

```powershell
npm.cmd install
npm.cmd run dev
npm.cmd run lint
npm.cmd run test
npm.cmd run build
```

O servidor local usa a porta `5173`.
