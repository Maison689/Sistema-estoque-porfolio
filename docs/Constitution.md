# Constitution.md

# Constituição de Desenvolvimento

## Objetivo

Este documento define os princípios fundamentais de desenvolvimento do
projeto. Toda implementação deverá respeitar estas diretrizes
independentemente da tecnologia utilizada.

------------------------------------------------------------------------

# 1. Simplicidade

Sempre priorizar código simples em vez de soluções complexas.

-   Resolver o problema da forma mais direta possível.
-   Evitar abstrações desnecessárias.
-   Não otimizar prematuramente.

> Regra: se duas soluções resolvem o mesmo problema, a mais simples deve
> ser escolhida.

------------------------------------------------------------------------

# 2. Legibilidade

Código é escrito para pessoas.

-   Nomes claros e descritivos.
-   Funções pequenas e com responsabilidade única.
-   Evitar comentários para explicar código confuso; prefira torná-lo
    claro.

------------------------------------------------------------------------

# 3. Segurança

Nunca armazenar:

-   senhas;
-   tokens;
-   chaves de API;
-   credenciais;

diretamente no código (hardcode).

Utilizar mecanismos apropriados para gerenciamento de segredos.

Nunca registrar informações sensíveis em logs.

------------------------------------------------------------------------

# 4. Responsabilidade Única

Cada função, módulo ou componente deve possuir apenas uma
responsabilidade bem definida.

------------------------------------------------------------------------

# 5. Não se Repita (DRY)

Evitar duplicação de lógica.

Quando um comportamento for reutilizado, extraí-lo para uma
implementação compartilhada quando isso realmente simplificar a
manutenção.

------------------------------------------------------------------------

# 6. Não Antecipar Necessidades (YAGNI)

Não implementar funcionalidades "que poderão ser úteis no futuro".

Implementar apenas o que foi aprovado.

------------------------------------------------------------------------

# 7. Alteração Mínima

Modificar apenas o necessário para atender à tarefa.

Não realizar refatorações paralelas sem aprovação.

------------------------------------------------------------------------

# 8. Consistência

Seguir padrões já estabelecidos no projeto.

Novos padrões somente poderão ser introduzidos mediante aprovação.

------------------------------------------------------------------------

# 9. Tratamento de Erros

-   Nunca ocultar erros silenciosamente.
-   Mensagens devem ser claras.
-   Erros inesperados devem ser propagados ou registrados adequadamente.

------------------------------------------------------------------------

# 10. Performance Consciente

Buscar soluções eficientes, mas sem sacrificar simplicidade e
legibilidade.

Otimizações devem ser motivadas por necessidade comprovada.

------------------------------------------------------------------------

# 11. Documentação

Toda alteração que modificar comportamento, arquitetura, regras de
negócio ou integrações deverá refletir na documentação correspondente.

------------------------------------------------------------------------

# 12. Revisão Mental

Antes de considerar uma implementação concluída, o agente deve
verificar:

-   O código ficou mais simples?
-   Está fácil de entender?
-   Introduziu duplicação?
-   Criou riscos de segurança?
-   Respeita os padrões do projeto?
-   Existe uma solução menor para o mesmo problema?

------------------------------------------------------------------------

# Princípio Fundamental

Todo código produzido deve ser simples, seguro, legível, consistente e
facilmente mantido por outra pessoa.
