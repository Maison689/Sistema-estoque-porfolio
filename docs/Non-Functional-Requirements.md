# Requisitos Não Funcionais — Sis Estoque

## Controle do documento

- **Status:** Aprovado para orientar a Meta 2
- **Escopo:** MVP de portfólio
- **Referência:** `Architecture.md`

Este documento registra somente metas não funcionais essenciais e verificáveis.
Princípios de desenvolvimento permanecem em `Constitution.md`.

## 1. Performance

- Operações comuns da API devem responder em até 500 ms no percentil 95, em
  ambiente e volume de demonstração documentados.
- Consultas do dashboard devem responder em até 2 segundos.
- Listagens com crescimento potencial devem ser paginadas.
- A paginação padrão será de 20 registros e terá limite máximo de 100.
- Filtros e ordenações que afetem a coleção completa devem ser executados no
  backend.
- A interface deve apresentar feedback enquanto uma operação estiver em
  andamento.
- Otimizações adicionais somente serão feitas após medição que demonstre a
  necessidade.

## 2. Segurança

- Rotas protegidas exigem autenticação e autorização validada pela API.
- Senhas devem ser armazenadas somente como hash seguro, nunca em texto puro.
- Senhas, tokens, chaves e strings de conexão devem ser fornecidos por variáveis
  de ambiente e não podem ser versionados.
- Produção deve utilizar HTTPS.
- CORS deve permitir apenas as origens necessárias em cada ambiente.
- Toda entrada externa deve ser validada pelo backend.
- Erros e logs não podem expor senha, token, SQL, stack trace ou configuração
  sensível.
- Dependências devem possuir versões controladas e passar por verificação de
  vulnerabilidades antes do deploy.
- O mecanismo de autenticação será definido e aprovado na fase correspondente,
  conforme `Architecture.md`.

## 3. Responsividade

- Os fluxos principais devem funcionar em desktop, tablet e celular.
- A menor largura suportada será de 360 px.
- A página não deve exigir rolagem horizontal para executar ações principais.
- Tabelas extensas podem usar rolagem interna indicada, cartões ou outra
  apresentação adaptada.
- Ações essenciais devem funcionar por teclado.
- Campos devem possuir rótulos, foco visível e mensagens de erro identificáveis.
- Informações e estados não podem depender somente de cor.
- Carregamento, conteúdo vazio, erro e falta de permissão devem possuir estados
  visuais distintos.

## 4. Escalabilidade

- O backend permanecerá um monólito modular durante o MVP.
- PostgreSQL será a fonte oficial dos dados persistidos.
- Consultas devem usar paginação, filtros no banco e índices justificados pelas
  consultas reais.
- Conexões com o banco devem ser gerenciadas e encerradas corretamente.
- O backend deve evitar estado apenas em memória quando isso impedir mais de uma
  instância no futuro.
- Microsserviços, filas, cache distribuído, particionamento e orquestração de
  contêineres não fazem parte do MVP.
- Docker será introduzido somente na fase de deploy.
- Qualquer expansão arquitetural exigirá evidência de necessidade, análise de
  impacto e aprovação explícita.

Este documento está aprovado para orientar a Meta 2, com metas de tempo,
segurança, largura mínima e limites de escalabilidade validados.
