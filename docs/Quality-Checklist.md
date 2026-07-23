# Checklist de Qualidade

Registro de verificacao da Meta 10.

## Escopo Revisado

| Area | Evidencia |
|---|---|
| Autenticacao e autorizacao | Testes de login, usuario atual, administracao de usuarios e bloqueio por perfil. |
| Categorias e produtos | Testes de unicidade, permissao, categoria ativa e saldo inicial zero. |
| Fornecedores e vinculos | Testes de documento fiscal, duplicidade, inativacao e vinculos. |
| Movimentacoes | Testes de entrada, saida, ajuste, saldo insuficiente, produto inativo, filtros e paginacao. |
| Dashboard | Testes de permissao e calculo com dados oficiais. |
| Frontend | Testes de login, navegacao, permissoes, catalogo, fornecedores, movimentacoes e dashboard. |

## Comandos Obrigatorios

Backend:

```powershell
cd backend
.\.venv\Scripts\ruff.exe check app migrations
.\.venv\Scripts\pytest.exe
.\.venv\Scripts\alembic.exe current
```

Frontend:

```powershell
cd frontend
npm.cmd run lint
npm.cmd run test
npm.cmd run build
```

## Seguranca

- Arquivos `.env` reais permanecem ignorados pelo Git.
- Somente `.env.example` deve ser versionado.
- Senhas reais nao aparecem na documentacao.
- O administrador inicial e criado por variaveis de ambiente locais.
- O script de dados demo usa usuario existente informado por variavel de ambiente.
- Operacoes restritas tambem sao bloqueadas no backend.

## Dependencias

- Dependencias do backend estao fixadas em `backend/requirements.txt`.
- Dependencias do frontend estao registradas em `frontend/package-lock.json`.
- Nenhuma dependencia de producao foi adicionada na Meta 10.

## CI

CI no GitHub permanece pendente porque o plano aprovado exige autorizacao
especifica para criar workflows e executar acoes externas.

## Definition of Done

A Meta 10 pode ser considerada concluida quando:

- comandos obrigatorios passam;
- documentacao de instalacao, API e validacao esta atualizada;
- screenshots do MVP estao disponiveis;
- nenhuma credencial real foi rastreada;
- pendencias externas estao explicitadas.

## Resultado da Meta 10

Executado em 23/07/2026:

- `ruff check app scripts migrations`: aprovado;
- `pip check`: aprovado;
- `pytest`: 18 testes aprovados, com 1 aviso conhecido do Starlette TestClient;
- `alembic current`: `20260720_0004 (head)`;
- `oxlint`: aprovado;
- `vitest run`: 7 testes aprovados;
- `tsc -b`: aprovado;
- `vite build`: aprovado;
- `npm audit --audit-level=high`: 0 vulnerabilidades;
- screenshots desktop e mobile gerados em `docs/screenshots`;
- verificacao visual dos screenshots de dashboard desktop e mobile concluida.
