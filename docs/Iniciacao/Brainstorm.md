---
id: brainstorm
title: Brainstorm
---

## Introdução

O brainstorm é uma técnica de elicitação de requisitos que consiste em reunir a equipe e discutir sobre diversos tópicos gerais do projeto apresentados no Documento de Problema de Negócio. No brainstorm, o diálogo é incentivado e críticas são evitadas, permitindo que todos colaborem com suas próprias ideias.

## Metodologia

A equipe se reuniu para debater ideias gerais sobre o projeto via Discord. A sessão começou às 19h do dia 20/09/2025 e terminou às 20h30.

## Brainstorm

### Perguntas

#### 1. Qual o objetivo principal da aplicação?

- Alunos precisam de ajuda para se localizar; monitores precisam de organização; a equipe CASAS precisa de automatização de processos (muitas planilhas); professores e coordenadores precisam de visibilidade e gerenciamento do processo.
- A plataforma deve fornecer automatização de processos custosos.
- O objetivo da aplicação é centralizar as informações das monitorias e servir como um guia para os alunos.
- Permitir que a equipe CASAS acompanhe o progresso dos alunos monitorados.
- Gerenciar todo o processo burocrático das monitorias.

#### 2. Como será o processo para cadastrar um novo monitor?

- O professor terá acesso ao histórico completo do aluno e, com base nas regras de negócio, aprovará ou não a candidatura.

#### 3. Quais são as funcionalidades MAIS importantes para serem entregues?

- **Para o Aluno:** acesso a todas as informações possíveis (sala da monitoria, horário, nome do monitor).  
- **Para o Coordenador:** cadastrar disciplinas, escalas de horários, aprovar total de horas de cada monitor no semestre.  
- **Para o Professor:** editar e gerenciar escalas de horários, aprovar/reprovar candidaturas e disponibilizar material de apoio.  
- **Para o Sistema:** enviar notificações 24h e 1h antes da monitoria para alunos e monitores, diminuindo esquecimentos e faltas.  
- **Para o Monitor:** visualizar horários e dias das aulas, enviar/receber atividades, notificar ausência e registrar presença.

### Requisitos Elicitados

| ID   | Descrição |
|------|-----------|
| BS01 | O sistema deve exibir para o aluno todas as informações da monitoria (sala, horário, nome do monitor). |
| BS02 | O sistema deve enviar notificações de lembrete 24h e 1h antes de cada monitoria agendada. |
| BS03 | O sistema deve permitir que um aluno se candidate para uma vaga de monitor. |
| BS04 | No processo de candidatura, o sistema deve validar se o CR geral do aluno é ≥ 8.0 e o CR do período é ≥ 7.0. |
| BS05 | O monitor deve ter uma interface para definir seus horários e dias de disponibilidade e notificar ausências, sendo automaticamente informado a todos os alunos. |
| BS06 | O professor deve poder enviar indicações de alunos para serem monitores através de um formulário. |
| BS07 | O coordenador deve ter um dashboard com estatísticas sobre as monitorias (opcional). |
| BS08 | O coordenador deve ter funcionalidade para aprovar o relatório de horas dos monitores. |
| BS09 | O sistema deve permitir que o monitor envie e receba atividades. |
| BS10 | O sistema deve permitir que o aluno envie e receba atividades. |

## Conclusão

A aplicação da técnica permitiu elicitar os primeiros requisitos do projeto, proporcionando clareza sobre as necessidades de cada usuário.

## Referências Bibliográficas

- BARBOSA, S. D. J.; DA SILVA, B. S. *Interação Humano-Computador*. Elsevier, 2010.

## Autor(es)

| Data        | Versão | Descrição           | Autor(es)                                   |
|------------|--------|-------------------|--------------------------------------------|
| 13/09/2025 | 1.0    | Criação do documento | XXX XXXX, XXXX XXXX, YYY YYYY e ZZZ XXXX  |
