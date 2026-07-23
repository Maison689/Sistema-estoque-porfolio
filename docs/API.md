# API Sis Estoque

Base local: `http://127.0.0.1:8000/api/v1`

Autenticacao: token Bearer obtido em `POST /auth/login`.

## Saude

| Metodo | Rota | Perfil | Descricao |
|---|---|---|---|
| GET | `/health` | Publico | Verifica se a API responde. |

## Autenticacao e usuarios

| Metodo | Rota | Perfil | Descricao |
|---|---|---|---|
| POST | `/auth/login` | Publico | Autentica usuario ativo e retorna token. |
| GET | `/auth/me` | Autenticado | Retorna usuario atual sem senha/hash. |
| POST | `/auth/logout` | Autenticado | Encerra a sessao no cliente. |
| GET | `/users` | Administrador | Lista usuarios. |
| POST | `/users` | Administrador | Cria usuario. |
| PATCH | `/users/{user_id}` | Administrador | Atualiza usuario, perfil, status ou senha. |

## Categorias e produtos

| Metodo | Rota | Perfil | Descricao |
|---|---|---|---|
| GET | `/categories` | Autenticado | Lista categorias com filtros por busca/status. |
| POST | `/categories` | Administrador/Gestor | Cria categoria unica por nome normalizado. |
| PATCH | `/categories/{category_id}` | Administrador/Gestor | Atualiza ou inativa categoria. |
| GET | `/products` | Autenticado | Lista produtos com filtros por busca, categoria e estoque. |
| POST | `/products` | Administrador/Gestor | Cria produto ativo com saldo inicial `0.000`. |
| PATCH | `/products/{product_id}` | Administrador/Gestor | Atualiza dados cadastrais do produto. |

Filtro de estoque aceito em `/products`: `stock_status=below_minimum` ou
`stock_status=within_minimum`.

## Fornecedores

| Metodo | Rota | Perfil | Descricao |
|---|---|---|---|
| GET | `/suppliers` | Autenticado | Lista fornecedores com busca/status. |
| POST | `/suppliers` | Administrador/Gestor | Cria fornecedor com CPF/CNPJ opcional validado. |
| PATCH | `/suppliers/{supplier_id}` | Administrador/Gestor | Atualiza ou inativa fornecedor. |
| GET | `/products/{product_id}/suppliers` | Autenticado | Lista fornecedores vinculados ao produto. |
| POST | `/products/{product_id}/suppliers` | Administrador/Gestor | Vincula fornecedor ativo a produto ativo. |
| DELETE | `/products/{product_id}/suppliers/{supplier_id}` | Administrador/Gestor | Remove vinculo produto-fornecedor. |

## Movimentacoes

| Metodo | Rota | Perfil | Descricao |
|---|---|---|---|
| GET | `/movements` | Autenticado | Lista historico paginado e filtravel. |
| POST | `/movements/entries` | Autenticado | Registra entrada de estoque. |
| POST | `/movements/exits` | Autenticado | Registra saida sem permitir saldo negativo. |
| POST | `/movements/adjustments` | Administrador/Gestor | Registra ajuste com justificativa. |

Filtros aceitos em `/movements`:

- `product_id`
- `type`: `ENTRY`, `EXIT` ou `ADJUSTMENT`
- `created_by_id`
- `date_from` e `date_to` em formato ISO
- `limit` entre 1 e 100
- `offset` maior ou igual a 0

Resposta paginada:

```json
{
  "items": [],
  "limit": 20,
  "offset": 0,
  "total": 0
}
```

## Dashboard

| Metodo | Rota | Perfil | Descricao |
|---|---|---|---|
| GET | `/dashboard` | Administrador/Gestor | Retorna indicadores oficiais do estoque. |

O dashboard consolida:

- produtos ativos e inativos;
- produtos ativos abaixo do minimo;
- total de movimentacoes;
- resumo de movimentacoes por tipo;
- ultimas movimentacoes;
- lista de produtos abaixo do minimo.
