# Guia da Documentação — Sis Estoque

## Objetivo

Este arquivo orienta a consulta dos documentos do projeto. Ele informa a
finalidade de cada documento, quando consultá-lo e quais fontes são obrigatórias
para cada tipo de tarefa.

Este guia não substitui os documentos originais. Em caso de dúvida, a decisão
deve ser tomada a partir da fonte aplicável e da ordem de precedência definida
em `AGENTS.md`.

## 1. Documentos do projeto

| Documento | Objetivo | Quando consultar |
|---|---|---|
| `AGENTS.md` | Define o processo SDD, níveis de risco, aprovações obrigatórias, verificações e limites de atuação. | Antes de iniciar qualquer tarefa, inclusive alterações exclusivamente documentais. |
| `Constitution.md` | Define os princípios permanentes de simplicidade, segurança, legibilidade, consistência e alteração mínima. | Antes de planejar, implementar ou revisar qualquer alteração. |
| `Product-Vision.md` | Explica problema, público-alvo, objetivo, proposta de valor, escopo e critérios de sucesso do MVP. | Ao avaliar novas funcionalidades, prioridade, escopo ou aderência ao produto. |
| `Tech-Stack.md` | Registra as tecnologias e versões oficiais do projeto. | Antes de configurar ambiente, adicionar dependências, criar projetos ou alterar ferramentas. |
| `Architecture.md` | Define componentes, responsabilidades, módulos, integrações, fluxo de requisições e decisões arquiteturais. | Antes de alterar estrutura, contratos, autenticação, persistência, integrações ou deploy. |
| `Use-Cases.md` | Descreve atores, fluxos, exceções e critérios de aceitação do comportamento esperado. | Antes de implementar ou testar um fluxo utilizado pelo usuário. |
| `Business-Rules.md` | Define as regras que controlam permissões, cadastros, saldo, movimentações e consultas. | Antes de alterar comportamento do sistema, validações ou permissões. |
| `Data-Model.md` | Define entidades, campos, relacionamentos, constraints, transações e decisões aprovadas do banco. | Antes de alterar models, persistência, consultas, migrations ou integridade dos dados. |
| `Non-Functional-Requirements.md` | Define metas essenciais de performance, segurança, responsividade e escalabilidade. | Ao implementar, testar ou revisar qualquer uma dessas características. |
| `Execution-Plan.md` | Organiza o projeto em metas, dependências, critérios de conclusão e gates de aprovação. | Antes de iniciar uma nova fase e ao acompanhar o andamento do projeto. |

## 2. Documentos obrigatórios por tipo de tarefa

`AGENTS.md` e `Constitution.md` são obrigatórios para **todas** as tarefas. A
tabela abaixo apresenta os documentos adicionais mínimos.

| Tipo de tarefa | Documentos adicionais obrigatórios |
|---|---|
| Definição de produto, escopo ou nova funcionalidade | `Product-Vision.md`, `Use-Cases.md`, `Business-Rules.md`, `Execution-Plan.md` |
| Planejamento de uma meta | `Execution-Plan.md` e todos os documentos relacionados ao conteúdo da meta |
| Interface e frontend | `Tech-Stack.md`, `Architecture.md`, `Use-Cases.md`, `Non-Functional-Requirements.md` |
| Backend e API | `Tech-Stack.md`, `Architecture.md`, `Use-Cases.md`, `Business-Rules.md`, `Data-Model.md` |
| Regra de negócio ou validação | `Business-Rules.md`, `Use-Cases.md`, `Data-Model.md` quando houver dados persistidos |
| Banco, model ou migration | `Data-Model.md`, `Business-Rules.md`, `Architecture.md`, `Tech-Stack.md` |
| Autenticação, autorização ou segurança | `Architecture.md`, `Business-Rules.md`, `Use-Cases.md`, `Data-Model.md`, `Non-Functional-Requirements.md` |
| Performance ou escalabilidade | `Non-Functional-Requirements.md`, `Architecture.md`, `Data-Model.md` quando envolver consultas ou banco |
| Responsividade ou acessibilidade | `Non-Functional-Requirements.md`, `Use-Cases.md`, `Architecture.md` |
| Dependência, ferramenta ou estrutura do projeto | `Tech-Stack.md`, `Architecture.md`, `Execution-Plan.md` |
| Configuração do ambiente local | `Tech-Stack.md`, `Architecture.md`, `Execution-Plan.md` |
| Git ou GitHub | `Execution-Plan.md` e a seção de aprovações de `AGENTS.md` |
| Deploy ou Docker | `Architecture.md`, `Non-Functional-Requirements.md`, `Execution-Plan.md`, `Tech-Stack.md` |
| Correção de defeito | Especificação do comportamento afetado: `Use-Cases.md`, `Business-Rules.md`, `Data-Model.md` ou `Non-Functional-Requirements.md`, conforme o caso |
| Testes | Documento que define o comportamento testado e `Architecture.md` para a estratégia técnica aplicável |
| Alteração exclusivamente documental | Documento fonte do assunto e todos os documentos que possuam referências ou definições potencialmente afetadas |

## 3. Como escolher documentos adicionais

A tabela define o conjunto mínimo. Uma tarefa deve consultar também qualquer
documento que possa ser afetado indiretamente.

Exemplos:

- Uma alteração visual simples consulta os documentos de frontend. Se mudar o
  fluxo do usuário, `Use-Cases.md` e `Business-Rules.md` também são obrigatórios.
- Uma alteração em endpoint consulta os documentos de backend. Se mudar campos
  persistidos, `Data-Model.md` também é obrigatório.
- Uma correção de saldo exige, no mínimo, `Business-Rules.md`, `Use-Cases.md`,
  `Data-Model.md` e `Architecture.md`.
- Uma nova dependência exige consulta a `Tech-Stack.md`, análise arquitetural e
  aprovação específica antes da instalação.

Se houver dúvida sobre o impacto, deve-se consultar o conjunto mais abrangente
antes de preparar o plano.

## 4. Ordem de precedência

Quando houver divergência, seguir esta ordem:

1. políticas de segurança, privacidade, integridade e instruções superiores;
2. solicitação atual e aprovações explícitas do responsável;
3. especificações e critérios de aceitação aprovados;
4. `Constitution.md`;
5. `Architecture.md` e `Tech-Stack.md`;
6. documentação, testes, contratos e padrões existentes;
7. preferências de implementação.

Uma fonte de nível inferior não pode substituir silenciosamente uma decisão de
nível superior. Conflitos que alterem comportamento, segurança, arquitetura ou
dados devem ser apresentados para decisão humana.

## 5. Fluxo obrigatório do SDD

Toda mudança segue este fluxo:

1. **Compreender:** ler os documentos obrigatórios e inspecionar o estado atual.
2. **Esclarecer:** identificar dúvidas que possam alterar o resultado.
3. **Planejar:** apresentar objetivo, impacto, arquivos, riscos e verificações.
4. **Aguardar aprovação:** nenhuma alteração ocorre antes da aprovação explícita
   posterior ao plano.
5. **Executar:** implementar somente o escopo aprovado.
6. **Verificar:** executar os testes, análises e builds previstos.
7. **Relatar:** informar alterações, resultados, limitações e pendências.

Instalação de dependências, migrations, autenticação, GitHub, deploy, push,
merge e publicação exigem a autorização correspondente descrita em `AGENTS.md`.

## 6. Manutenção da documentação

- Alterações de comportamento devem atualizar casos de uso e regras afetadas.
- Alterações de dados devem atualizar `Data-Model.md` e regras relacionadas.
- Alterações arquiteturais devem atualizar `Architecture.md`.
- Alterações de tecnologia devem atualizar `Tech-Stack.md` e documentação de
  instalação aplicável.
- Alterações de metas ou sequência devem atualizar `Execution-Plan.md`.
- Requisitos não devem ser duplicados em vários documentos sem necessidade.
- Decisões ainda não aprovadas devem permanecer identificadas como pendentes.
- Referências e identificadores devem ser revisados após renumerações.
- Documentos alterados devem passar por revisão cruzada com suas fontes.

O objetivo é manter cada informação em uma fonte clara, simples e rastreável.
