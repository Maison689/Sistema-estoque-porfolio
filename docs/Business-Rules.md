# Regras de Negócio — Sis Estoque

## Controle do documento

- **Status:** Aprovado para orientar a Meta 2
- **Escopo:** MVP
- **Fonte relacionada:** `Product-Vision.md`

Este documento contém somente regras que definem o comportamento do sistema.
Decisões técnicas permanecem em `Architecture.md` e princípios gerais em
`Constitution.md`.

## 1. Usuários e permissões

| ID | Regra |
|---|---|
| RN-001 | Operações protegidas exigem usuário autenticado e ativo. |
| RN-002 | O e-mail do usuário é obrigatório e único, sem diferenciar maiúsculas e minúsculas. |
| RN-003 | Cada usuário possui um dos perfis: Administrador, Gestor ou Operador. |
| RN-004 | Somente Administradores podem cadastrar, alterar perfil, ativar ou inativar usuários. |
| RN-005 | Toda operação deve respeitar a matriz de permissões, com validação obrigatória pela API. |

### Matriz de permissões

| Operação | Administrador | Gestor | Operador |
|---|:---:|:---:|:---:|
| Administrar usuários | Sim | Não | Não |
| Consultar cadastros | Sim | Sim | Sim |
| Manter categorias, produtos e fornecedores | Sim | Sim | Não |
| Registrar entrada | Sim | Sim | Sim |
| Registrar saída | Sim | Sim | Sim |
| Registrar ajuste | Sim | Sim | Não |
| Consultar histórico | Sim | Sim | Sim |
| Consultar dashboard gerencial | Sim | Sim | Não |

## 2. Categorias e produtos

| ID | Regra |
|---|---|
| RN-006 | O nome da categoria é obrigatório e único, sem diferenciar maiúsculas e minúsculas. |
| RN-007 | Todo produto pertence a exatamente uma categoria ativa no momento do cadastro ou da alteração. |
| RN-008 | Todo produto possui nome, SKU, unidade de medida e estoque mínimo. As unidades aceitas no MVP são `UN`, `CX`, `KG`, `G`, `L`, `ML`, `M` e `CM`. |
| RN-009 | O SKU é obrigatório e único, sem diferenciar maiúsculas e minúsculas. |
| RN-010 | O estoque mínimo não pode ser negativo. |
| RN-011 | Um novo produto começa com saldo zero; o estoque inicial deve ser registrado como entrada. |
| RN-012 | Categorias e produtos com vínculos ou histórico devem ser inativados, não apagados; produtos inativos não recebem movimentações. Categorias com produtos ativos não podem ser inativadas. |

## 3. Fornecedores

| ID | Regra |
|---|---|
| RN-013 | Todo fornecedor possui nome. Documento fiscal, e-mail e telefone são opcionais; quando o documento fiscal for informado, deve ser CPF ou CNPJ válido e único. |
| RN-014 | Um fornecedor pode atender vários produtos e um produto pode possuir vários fornecedores, sem vínculo duplicado. |
| RN-015 | Fornecedores inativos não recebem novos vínculos, mas seus dados e vínculos anteriores são preservados. |

## 4. Saldo e movimentações

| ID | Regra |
|---|---|
| RN-016 | O saldo de um produto só pode mudar por meio de uma movimentação. |
| RN-017 | O MVP possui movimentações de entrada, saída e ajuste. |
| RN-018 | Toda movimentação registra produto, variação, tipo, saldos anterior e resultante, responsável e data/hora. |
| RN-019 | Entradas têm variação positiva, saídas têm variação negativa e nenhuma movimentação pode ter variação zero. |
| RN-020 | Ajustes podem aumentar ou reduzir o saldo e exigem justificativa. |
| RN-021 | O saldo resultante nunca pode ser negativo. |
| RN-022 | Movimentação e atualização do saldo devem ser concluídas na mesma transação ou totalmente desfeitas. |
| RN-023 | Movimentações concorrentes do mesmo produto não podem utilizar o mesmo saldo anterior. |
| RN-024 | Uma movimentação concluída não pode ser editada ou apagada; correções são feitas por um novo ajuste. |
| RN-025 | O saldo armazenado deve coincidir com o resultado da última movimentação do produto. |

## 5. Consultas e dashboard

| ID | Regra |
|---|---|
| RN-026 | Um produto ativo está abaixo do mínimo quando seu saldo é menor que o estoque mínimo. |
| RN-027 | O histórico pode ser filtrado por produto, tipo, período e responsável. |
| RN-028 | Listagens com crescimento potencial devem ser paginadas. |
| RN-029 | Indicadores do dashboard devem ser calculados com os mesmos dados oficiais das consultas e não podem apresentar valores fictícios. |
| RN-030 | Produtos, fornecedores e usuários inativos continuam identificáveis nos registros históricos. |

## 6. Decisões aprovadas

| ID | Decisão | Impacto |
|---|---|---|
| DN-001 | Quantidades aceitam casas decimais com precisão de 12 dígitos e 3 casas decimais. | Saldo, estoque mínimo e movimentações |
| DN-002 | As unidades aceitas no MVP são `UN`, `CX`, `KG`, `G`, `L`, `ML`, `M` e `CM`. | Cadastro e apresentação de produtos |
| DN-003 | Fornecedor exige `name`; `tax_id`, `email` e `phone` são opcionais. Quando `tax_id` for informado, aceitar CPF ou CNPJ válido e único. | Cadastro e validação de fornecedores |
| DN-004 | A inativação de categoria com produtos ativos será bloqueada. | Manutenção de categorias |
| DN-005 | Operadores não acessam o dashboard gerencial; acessam somente consultas operacionais permitidas. | Permissões e navegação |
| DN-006 | Os limites máximos dos campos textuais estão definidos na tabela abaixo. | Banco, API e formulários |

### Limites máximos de campos textuais

| Campo | Limite |
|---|---:|
| Nome de usuário, categoria, produto ou fornecedor | 120 caracteres |
| E-mail | 254 caracteres |
| SKU | 64 caracteres |
| Unidade de medida | 10 caracteres |
| Descrição, observação ou justificativa | 500 caracteres |
| Telefone | 30 caracteres |
| Documento fiscal normalizado | 20 caracteres |

## 7. Critério de aprovação

Este documento está aprovado para orientar a Meta 2. Cada regra implementada
deverá ser coberta pelos casos de uso e testes aplicáveis.
