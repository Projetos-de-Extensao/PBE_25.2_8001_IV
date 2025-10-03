# Casos de Uso - SGM Ibmec

## UC01: Aluno Busca e se Inscreve em uma Monitoria

### Atores:
-   **Aluno**
-   **Sistema**

### Pré-Condições:
-   O Aluno deve estar autenticado no sistema.

### Fluxo Básico:
1.  O Aluno acessa a funcionalidade "Buscar Monitoria".
2.  O Sistema exibe as opções de filtro (ex: por disciplina).
3.  O Aluno seleciona a disciplina desejada.
4.  O Sistema exibe as informações da monitoria encontrada (Horário, Monitor, Sala).
5.  O Aluno clica no botão "Inscrever-se".
6.  O Sistema apresenta uma tela de confirmação.
7.  O Aluno confirma sua inscrição.
8.  O Sistema registra a inscrição, envia uma notificação para o Monitor e uma confirmação para o Aluno.

### Fluxos Alternativos:
-   **4a. Nenhuma monitoria encontrada para os filtros selecionados.**
    1.  O Sistema exibe a mensagem "Nenhuma monitoria encontrada para sua busca."
-   **7a. A monitoria atinge o limite de vagas momentos antes da confirmação.**
    1.  O Sistema exibe a mensagem "Esta monitoria não possui mais vagas disponíveis" e atualiza a tela de informações.

---

## UC02: Monitor Define sua Disponibilidade

### Atores:
-   **Monitor**
-   **Sistema**

### Pré-Condições:
-   O Monitor deve estar autenticado e ter seu cadastro aprovado.

### Fluxo Básico:
1.  O Monitor acessa seu painel e seleciona a opção "Gerenciar Agenda".
2.  O Sistema exibe uma interface de calendário semanal/mensal (com horários predefinidos para sua escolha).
3.  O Monitor clica nos dias e horários em que deseja oferecer monitoria, marcando-os como "Disponível".
4.  O Monitor salva suas alterações.
5.  O Sistema atualiza a agenda do Monitor, tornando os horários selecionados visíveis para os Alunos.

### Fluxos Alternativos:
-   **3a. O Monitor tenta marcar um horário que já possui uma aula agendada.**
    1.  O Sistema não permite a alteração e exibe um aviso.
-   **3b. O Monitor precisa remover um horário que estava disponível.**
    1.  O Monitor clica em um horário "Disponível" para removê-lo.
    2.  Se o horário já tiver uma aula agendada, o Sistema exigirá o cancelamento da aula antes de remover a disponibilidade (ver caso de uso "Cancelar Agendamento").

---

## UC03: Coordenador Aprova Horas do Monitor

### Atores:
-   **Coordenador**
-   **Sistema**

### Pré-Condições:
-   O Coordenador deve estar autenticado no sistema.
-   Deve existir pelo menos um relatório de horas submetido por um Monitor.

### Fluxo Básico:
1.  O Coordenador acessa seu Painel de Controle e navega para a seção "Aprovação de Horas".
2.  O Sistema exibe uma lista de Monitores com relatórios de horas pendentes de aprovação.
3.  O Coordenador seleciona um Monitor para visualizar o detalhamento das aulas ministradas no período.
4.  O Coordenador verifica os registros e clica no botão "Aprovar".
5.  O Sistema atualiza o status das horas para "Aprovadas" e envia uma notificação de confirmação ao Monitor.

### Fluxos Alternativos:
-   **4a. O Coordenador identifica uma inconsistência e clica em "Reprovar".**
    1.  O Sistema abre um campo para que o Coordenador justifique o motivo da reprovação.
    2.  O Coordenador escreve o motivo e confirma.
    3.  O Sistema atualiza o status das horas para "Reprovadas" e envia uma notificação ao Monitor, incluindo o motivo da reprovação para que ele possa corrigir.
