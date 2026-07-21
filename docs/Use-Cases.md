# Casos de Uso — Sis Estoque

## Controle do documento

- **Status:** Aprovado para orientar a Meta 2
- **Escopo:** MVP
- **Regras relacionadas:** `Business-Rules.md`

Este documento descreve o comportamento esperado sem definir detalhes de tela
ou de implementação. Os casos de uso só se tornam fonte aprovada para o código
depois da validação explícita de seus fluxos e critérios de aceitação.

## 1. Atores

| Ator | Objetivo |
|---|---|
| Administrador | Configurar acessos e executar qualquer operação do MVP |
| Gestor | Manter cadastros, acompanhar indicadores e controlar movimentações |
| Operador | Consultar o estoque e registrar entradas e saídas autorizadas |
| Sistema | Validar regras, persistir dados, calcular saldos e apresentar erros |

## 2. Premissas gerais

- Casos protegidos exigem usuário autenticado e ativo.
- O backend é responsável pela autorização e pelas regras de negócio.
- Listagens oferecem paginação quando o volume puder crescer.
- Erros de validação preservam os dados já digitados na interface sempre que
  possível.
- Nenhuma mudança de saldo ocorre fora de uma movimentação.

## 3. UC-001 — Autenticar usuário

- **Ator:** Administrador, Gestor ou Operador
- **Objetivo:** acessar o sistema com uma identidade válida.
- **Pré-condição:** usuário cadastrado e ativo.
- **Pós-condição de sucesso:** sessão autenticada criada com o perfil correto.

### Fluxo principal

1. O usuário informa e-mail e senha.
2. O sistema valida as credenciais e o estado do usuário.
3. O sistema inicia a sessão.
4. O usuário é direcionado para a área permitida ao seu perfil.

### Exceções

- Credenciais inválidas: negar acesso sem revelar qual campo está incorreto.
- Usuário inativo: negar acesso.
- Falha inesperada: não criar sessão e apresentar mensagem segura.

### Critérios de aceitação

- Credenciais válidas de usuário ativo permitem acesso.
- Credenciais inválidas ou usuário inativo não permitem acesso.
- A senha não aparece em resposta, URL ou log.

## 4. UC-002 — Administrar usuários

- **Ator:** Administrador
- **Objetivo:** cadastrar usuários, definir perfil e controlar seu estado.
- **Pré-condição:** Administrador autenticado.
- **Pós-condição de sucesso:** usuário criado ou atualizado conforme RN-001 a
  RN-005.

### Fluxo principal

1. O Administrador acessa a lista de usuários.
2. O sistema apresenta os usuários conforme filtros e paginação.
3. O Administrador cria ou seleciona um usuário.
4. Informa dados obrigatórios, perfil e estado.
5. O sistema valida e salva a alteração.

### Exceções

- E-mail já utilizado: rejeitar e identificar o campo em conflito.
- Tentativa de acesso por outro perfil: negar a operação.
- Tentativa de auto-inativação na sessão atual: rejeitar.

### Critérios de aceitação

- Somente Administradores acessam operações de manutenção de usuários.
- Alterações de perfil passam a valer nas novas verificações de autorização.
- Usuário inativado não inicia nova sessão válida.

## 5. UC-003 — Manter categorias

- **Ator:** Administrador ou Gestor
- **Objetivo:** organizar produtos em categorias.
- **Pós-condição de sucesso:** categoria criada, atualizada ou inativada.

### Fluxo principal

1. O ator consulta categorias com busca, estado e paginação.
2. Cria uma categoria ou seleciona uma existente.
3. Informa ou altera os dados permitidos.
4. O sistema valida unicidade e obrigatoriedade.
5. O sistema salva e confirma a operação.

### Exceções

- Nome duplicado: rejeitar a gravação.
- Categoria inexistente: retornar não encontrado.
- Categoria inativa selecionada para novo produto: rejeitar a associação.
- Categoria com produtos ativos selecionada para inativação: rejeitar a
  operação.

### Critérios de aceitação

- Categoria válida fica disponível para produtos.
- Inativação preserva produtos e histórico associados.
- Operador pode consultar, mas não alterar categorias.

## 6. UC-004 — Manter produtos

- **Ator:** Administrador ou Gestor
- **Objetivo:** cadastrar e manter os itens controlados no estoque.
- **Pré-condição:** existir uma categoria ativa.
- **Pós-condição de sucesso:** produto persistido sem alteração direta de saldo.

### Fluxo principal

1. O ator consulta produtos por busca, categoria, estado e situação de estoque.
2. Cria um produto ou seleciona um existente.
3. Informa nome, SKU, categoria, unidade, estoque mínimo e demais dados
   aprovados.
4. O sistema valida os dados e a categoria.
5. O sistema salva o produto com saldo inicial zero quando for novo.

### Exceções

- SKU duplicado: rejeitar e identificar o conflito.
- Estoque mínimo negativo: rejeitar.
- Categoria inexistente ou inativa: rejeitar.
- Tentativa de editar saldo pelo cadastro: não oferecer nem aceitar a operação.

### Critérios de aceitação

- Novo produto começa com saldo zero.
- Estoque inicial só é incluído por UC-007.
- Produto inativo permanece consultável, mas não recebe movimentações.

## 7. UC-005 — Manter fornecedores

- **Ator:** Administrador ou Gestor
- **Objetivo:** cadastrar e manter fornecedores.
- **Pós-condição de sucesso:** fornecedor criado, atualizado ou inativado.

### Fluxo principal

1. O ator consulta fornecedores por busca e estado.
2. Cria um fornecedor ou seleciona um existente.
3. Informa nome e, quando aplicável, documento fiscal, e-mail e telefone.
4. O sistema valida obrigatoriedade e unicidade.
5. O sistema salva e confirma a operação.

### Exceções

- Documento informado inválido ou duplicado: rejeitar.
- E-mail em formato inválido: rejeitar.
- Fornecedor inativo: preservar dados e vínculos existentes.

### Critérios de aceitação

- O fornecedor pode ser localizado após o cadastro.
- Inativação impede novos vínculos, sem apagar o histórico.

## 8. UC-006 — Associar fornecedor a produto

- **Ator:** Administrador ou Gestor
- **Objetivo:** informar quais fornecedores atendem cada produto.
- **Pré-condição:** produto e fornecedor existentes e ativos.
- **Pós-condição de sucesso:** vínculo ativo e sem duplicidade.

### Fluxo principal

1. O ator acessa os fornecedores de um produto.
2. Seleciona um fornecedor ativo ainda não vinculado.
3. O sistema valida os dois cadastros.
4. O sistema cria o vínculo e confirma a operação.

### Exceções

- Produto ou fornecedor inativo: rejeitar novo vínculo.
- Vínculo duplicado: não criar uma segunda associação.

### Critérios de aceitação

- Um produto pode ter vários fornecedores.
- Um fornecedor pode atender vários produtos.
- Remover o vínculo não remove os cadastros nem movimentações.

## 9. UC-007 — Registrar entrada de estoque

- **Ator:** Administrador, Gestor ou Operador
- **Objetivo:** aumentar o saldo de um produto por recebimento ou estoque
  inicial.
- **Pré-condição:** usuário autorizado e produto ativo.
- **Pós-condição de sucesso:** movimentação e novo saldo persistidos na mesma
  transação.

### Fluxo principal

1. O ator seleciona um produto ativo.
2. Informa quantidade positiva e observação quando aplicável.
3. O sistema lê e protege o saldo atual contra atualização concorrente.
4. O sistema calcula o novo saldo.
5. Registra a entrada com saldos anterior e resultante.
6. Atualiza o saldo e confirma a operação.

### Exceções

- Quantidade inválida ou zero: rejeitar.
- Produto inexistente ou inativo: rejeitar.
- Falha durante a transação: não persistir movimentação nem saldo parcial.

### Critérios de aceitação

- O saldo aumenta exatamente pela quantidade informada.
- A entrada aparece no histórico com data e responsável do servidor.
- Reenvio causado por erro não deve criar duplicidade silenciosa.

## 10. UC-008 — Registrar saída de estoque

- **Ator:** Administrador, Gestor ou Operador
- **Objetivo:** reduzir o saldo de um produto.
- **Pré-condição:** usuário autorizado, produto ativo e saldo suficiente.
- **Pós-condição de sucesso:** saída e novo saldo persistidos na mesma transação.

### Fluxo principal

1. O ator seleciona um produto ativo.
2. Informa quantidade positiva e observação quando aplicável.
3. O sistema protege e consulta o saldo atual.
4. O sistema confirma que o saldo é suficiente.
5. Registra a saída e atualiza o saldo na mesma transação.
6. Confirma a operação e apresenta o saldo resultante.

### Exceções

- Saldo insuficiente: rejeitar sem alterar dados.
- Quantidade inválida, produto inativo ou falha transacional: rejeitar sem
  alteração parcial.

### Critérios de aceitação

- O saldo nunca fica negativo.
- Duas saídas concorrentes não consomem o mesmo saldo disponível.
- A saída concluída fica registrada no histórico.

## 11. UC-009 — Registrar ajuste de estoque

- **Ator:** Administrador ou Gestor
- **Objetivo:** corrigir uma divergência preservando a rastreabilidade.
- **Pré-condição:** usuário autorizado e produto ativo.
- **Pós-condição de sucesso:** ajuste e novo saldo persistidos na mesma
  transação.

### Fluxo principal

1. O ator seleciona o produto.
2. Informa variação positiva ou negativa e justificativa obrigatória.
3. O sistema valida autorização, saldo resultante e justificativa.
4. Registra o ajuste com saldos anterior e resultante.
5. Atualiza o saldo e confirma a operação.

### Exceções

- Operador tenta ajustar: negar acesso.
- Justificativa ausente, variação zero ou saldo negativo: rejeitar.

### Critérios de aceitação

- Todo ajuste possui justificativa e responsável.
- O registro original que motivou a correção permanece inalterado.
- O saldo resultante nunca é negativo.

## 12. UC-010 — Consultar saldo e histórico

- **Ator:** Administrador, Gestor ou Operador
- **Objetivo:** entender o saldo atual e por que ele mudou.

### Fluxo principal

1. O ator localiza um produto.
2. O sistema apresenta saldo atual, estoque mínimo e estado.
3. O ator consulta seu histórico.
4. Aplica filtros por tipo, período ou responsável quando necessário.
5. O sistema apresenta movimentações paginadas em ordem temporal definida.

### Critérios de aceitação

- Cada item informa tipo, variação, saldo anterior, saldo resultante, data e
  responsável.
- Produtos e usuários inativos continuam identificáveis no histórico.
- O saldo exibido coincide com o último saldo resultante.

## 13. UC-011 — Consultar estoque abaixo do mínimo

- **Ator:** Administrador, Gestor ou Operador
- **Objetivo:** identificar produtos ativos que precisam de atenção.

### Fluxo principal

1. O ator acessa a consulta ou aplica o filtro de estoque mínimo.
2. O sistema compara saldo e mínimo dos produtos ativos.
3. Apresenta os itens abaixo do limite com identificação clara.

### Critérios de aceitação

- Apenas produtos ativos com saldo menor que o mínimo são listados.
- A informação é visualmente distinguível sem depender somente de cor.
- Uma movimentação ou alteração de mínimo atualiza o resultado da consulta.

## 14. UC-012 — Consultar dashboard

- **Ator:** Administrador ou Gestor
- **Objetivo:** obter uma visão resumida da operação.

### Fluxo principal

1. O ator acessa o dashboard.
2. O sistema consulta os dados oficiais do estoque.
3. Apresenta total de produtos ativos, produtos abaixo do mínimo, resumo de
   movimentações e atividades recentes aprovadas para o MVP.
4. O ator navega de um indicador para a consulta detalhada quando disponível.

### Exceções

- Sem dados: apresentar estado vazio, não valores simulados.
- Falha parcial ou total: identificar o conteúdo indisponível e permitir nova
  tentativa.

### Critérios de aceitação

- Indicadores correspondem às mesmas regras das consultas detalhadas.
- Operador sem permissão recebe acesso negado.
- O layout continua compreensível nos tamanhos de tela suportados.

## 15. UC-013 — Encerrar sessão

- **Ator:** Administrador, Gestor ou Operador
- **Objetivo:** finalizar o acesso autenticado.

### Fluxo principal

1. O usuário solicita sair.
2. O sistema encerra ou invalida a sessão conforme o mecanismo adotado.
3. O usuário retorna à entrada do sistema.

### Critérios de aceitação

- Recursos protegidos não permanecem acessíveis pela sessão encerrada.
- Dados sensíveis da sessão não ficam expostos na interface.

## 16. Rastreabilidade inicial

| Capacidade do MVP | Casos de uso |
|---|---|
| Produtos e categorias | UC-003 e UC-004 |
| Fornecedores | UC-005 e UC-006 |
| Entradas, saídas e ajustes | UC-007, UC-008 e UC-009 |
| Estoque mínimo | UC-011 |
| Dashboard | UC-012 |
| Histórico | UC-010 |
| Acesso por perfil | UC-001, UC-002 e UC-013 |

## 17. Critério de aprovação

Os casos de uso estão aprovados para orientar a Meta 2. A implementação de cada
fluxo deverá ser revisada contra os critérios de aceitação correspondentes.
