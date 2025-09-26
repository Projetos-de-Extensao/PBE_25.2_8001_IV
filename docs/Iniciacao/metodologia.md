# Metodologia de Desenvolvimento - Projeto SGM Ibmec

## 1. Introdução

Este documento descreve a metodologia de desenvolvimento de software adotada pela equipe do projeto **SGM Ibmec**. O objetivo é definir um processo de trabalho claro e eficiente, que promova a colaboração, a qualidade do código e a entrega de valor contínua ao longo do semestre.

A abordagem escolhida é um **híbrido de práticas ágeis**, combinando os pontos fortes do Scrum, Kanban e Extreme Programming (XP) para se adequar à natureza acadêmica e ao escopo do projeto.

## 2. Metodologia Híbrida Adotada

A equipe optou por não seguir uma única metodologia de forma rígida, mas sim por adotar um conjunto de práticas de diferentes frameworks ágeis que melhor se adaptam a uma equipe pequena com um prazo fixo. Nossa abordagem se baseia em três pilares:

-   **Scrum (para Gestão do Tempo e Rituais):** Usaremos o conceito de Sprints para organizar nosso trabalho em ciclos curtos e focados, garantindo entregas incrementais e previsibilidade.
-   **Kanban (para Visualização do Fluxo de Trabalho):** Utilizaremos um quadro Kanban para tornar o progresso de todas as tarefas visível para toda a equipe, identificando gargalos e gerenciando o fluxo de trabalho de forma contínua.
-   **Extreme Programming (XP) (para Qualidade Técnica):** Adotaremos práticas de XP para garantir que o software que construímos seja robusto, testável e de fácil manutenção.

---

## 3. Detalhamento das Práticas

### 3.1. Práticas de Scrum

Para organizar o projeto no tempo, adotaremos os seguintes elementos do Scrum:

-   **Sprints:** Nosso trabalho será dividido em **Sprints de 2 semanas**. Cada Sprint começará com um planejamento (Sprint Planning) e terminará com a entrega de um incremento funcional do software.
-   **Sprint Planning:** No início de cada Sprint, a equipe se reunirá para selecionar as Histórias de Usuário (User Stories) do backlog que serão desenvolvidas nas próximas duas semanas.
-   **Daily Stand-ups:** Faremos reuniões rápidas (15 minutos) três vezes por semana para sincronizar o trabalho, onde cada membro responde: "O que eu fiz desde a última reunião?", "O que vou fazer até a próxima?" e "Há algum impedimento?".
-   **Product Backlog:** Manteremos um backlog priorizado de todas as Histérias de Usuário (Épicos e User Stories) que precisam ser desenvolvidas.

### 3.2. Práticas de Kanban

Para gerenciar o fluxo de trabalho de forma visual, usaremos um quadro Kanban (no Trello, GitHub Projects ou similar) com as seguintes colunas:

| Coluna         | Descrição                                                                         |
| :------------- | :---------------------------------------------------------------------------------- |
| **Backlog** | Todas as tarefas e Histórias de Usuário do projeto, priorizadas.                    |
| **To Do** | Tarefas selecionadas para o Sprint atual.                                           |
| **In Progress**| A tarefa que um membro da equipe está desenvolvendo ativamente. (Limite: 1 por pessoa). |
| **In Review** | A tarefa foi concluída e precisa que outro membro da equipe a revise (Code Review).  |
| **Done** | A tarefa foi revisada, testada e integrada à branch principal do projeto.            |

### 3.3. Práticas de Extreme Programming (XP)

Para garantir a qualidade técnica do nosso código, adotaremos as seguintes práticas de XP:

-   **Test-Driven Development (TDD):** Sempre que possível, escreveremos os testes antes de escrever o código da funcionalidade, garantindo que nosso código seja testável e que os requisitos sejam atendidos.
-   **Pair Programming (Programação em Par):** Em tarefas complexas ou quando um membro da equipe estiver com dificuldades, trabalharemos em duplas no mesmo código para compartilhar conhecimento e melhorar a qualidade da solução.
-   **Continuous Integration (Integração Contínua):** Usaremos o Git de forma disciplinada, com branches para cada nova funcionalidade e pull requests para revisão. O código só será integrado à branch `main` após a revisão (Code Review) por outro membro da equipe.
-   **Código Coletivo:** Todo membro da equipe tem permissão para melhorar qualquer parte do código a qualquer momento, garantindo que o conhecimento sobre o sistema seja compartilhado.

## 4. Conclusão

A adoção desta metodologia híbrida permite que a equipe se beneficie da estrutura temporal do Scrum, da clareza visual do Kanban e da excelência técnica do XP. Este processo de trabalho foi desenhado para maximizar a produtividade, a qualidade e a colaboração, garantindo que o projeto SGM Ibmec seja entregue com sucesso dentro do prazo acadêmico.

## 5. Referências

> FARLEY, David. **Engenharia de Software Moderna: Uma Abordagem de Engenharia para o Desenvolvimento de Software**. Pearson, 2021.

## 6. Autores

| Data       | Versão | Descrição                                                       | Autor(es)                      |
| :--------- | :----- | :---------------------------------------------------------------- | :----------------------------- |
| 26/09/2025 | 1.0    | Criação do documento com a definição da metodologia híbrida ágil. | João Pedro |
