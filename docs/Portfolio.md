# Portfolio

## Nome

Sis Estoque

## Resumo

Sistema web de gerenciamento de estoque criado como projeto de portfolio, com
frontend React, backend FastAPI e PostgreSQL. O MVP cobre autenticacao,
permissoes, produtos, fornecedores, movimentacoes transacionais, dashboard e
consultas operacionais.

## Funcionalidades

- Login com token Bearer.
- Perfis Administrador, Gestor e Operador.
- Cadastro de categorias e produtos.
- Saldo inicial zero e bloqueio de edicao direta de saldo.
- Cadastro de fornecedores e vinculos com produtos.
- Entrada, saida e ajuste de estoque com historico.
- Bloqueio de saldo negativo.
- Historico paginado e filtravel.
- Dashboard gerencial com dados oficiais.
- Destaque de produtos abaixo do minimo.

## Stack

- React 19
- TypeScript
- Vite
- Python 3.13
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL 17

## Diferenciais Tecnicos

- Desenvolvimento guiado por especificacao.
- Regras de negocio documentadas antes da implementacao.
- Migrations versionadas.
- Permissoes aplicadas no backend e refletidas no frontend.
- Movimentacoes transacionais com saldo anterior e saldo final.
- Testes automatizados para fluxos criticos.
- Dados sensiveis mantidos fora do Git.

## Como Demonstrar

1. Abrir o frontend local.
2. Fazer login com um administrador local criado pelo script documentado.
3. Mostrar dashboard com produtos abaixo do minimo e movimentacoes recentes.
4. Criar ou consultar produto.
5. Registrar entrada e saida.
6. Conferir historico com saldo anterior, variacao e saldo final.
7. Mostrar que Operador nao acessa dashboard nem administracao.

## Screenshots

As imagens geradas para a Meta 10 ficam em `docs/screenshots`.

| Tela | Arquivo |
|---|---|
| Dashboard desktop | `docs/screenshots/dashboard.png` |
| Dashboard mobile | `docs/screenshots/dashboard-mobile.png` |
| Catalogo de produtos | `docs/screenshots/catalogo-produtos.png` |
| Movimentacoes | `docs/screenshots/movimentacoes.png` |
| Fornecedores | `docs/screenshots/fornecedores.png` |

## Proximos Passos

- Meta 11: deploy com Docker mediante plano e aprovacao especifica.
- CI no GitHub mediante aprovacao especifica de workflow e acoes externas.
- Endurecimento de producao: CORS, segredos, backup, logs e HTTPS.
