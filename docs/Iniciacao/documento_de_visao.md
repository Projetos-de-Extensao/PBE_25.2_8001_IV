---
id: documento_de_visao

title: Documento de Visão
---

## Introdução
O propósito deste documento é fornecer uma visão geral sobre o projeto. Sendo assim, nesse documento serão descritas de maneira resumida as principais funcionalidades, usabilidades, o problema que será abordado e os objetivos da equipe.

## Descrição do Problema
Com o aumento da demanda, a equipe CASAS vem enfrentando dificuldades em gerenciar e organizar inscrições, salas, horários, relatórios e a comunicação entre os atores envolvidos no processo de monitoria.

### Problema
Dificuldade em gerenciar e organizar inscrições, salas, horários, relatórios e comunicação entre os usuários do processo de monitoria.

### Impactados
- Alunos: não encontram as salas de monitoria facilmente.  
- Monitores: dificuldade em organizar horários.  
- Professores: desafios na indicação e acompanhamento dos alunos.  
- Coordenadores: aprovação de relatórios e visão geral das monitorias.  
- Equipe CASAS: excesso de trabalho administrativo (planilhas manuais).

### Consequência
- Os alunos perdem tempo desnecessário procurando as salas.  
- A equipe CASAS enfrenta trabalho administrativo excessivo e repetitivo.  

### Solução
Criar uma aplicação web que centraliza o processo de gestão de monitorias, trazendo automação de processos administrativos, centralizando informações e facilitando a localização de alunos, monitores e professores.

## Objetivos
- Centralizar informações de monitorias.  
- Melhorar a comunicação entre alunos, monitores, professores e coordenadores.  
- Automatizar processos burocráticos (candidatura, relatórios, aprovações).  

## Descrição do Usuário
- **Aluno:** procura, envia atividades, participa das monitorias e avalia monitores.  
- **Monitor:** se candidata, define disponibilidade, registra presença e notifica ausência.  
- **Professor:** recomenda alunos, acompanha monitorias e gerencia/edita a escala de horários (se necessário).  
- **Coordenador:** adiciona disciplinas, define escalas de horários e aprova horas complementares.  

## Recursos do Produto

### Gerenciamento de Conta
Cada usuário (Aluno, Monitor, Professor, Coordenador) terá um cadastro individual com login e senha. A autenticação permitirá acesso apenas às funcionalidades correspondentes ao seu perfil.

### Gerenciamento de Monitorias
O sistema deverá permitir a visualização de todas as informações relacionadas às monitorias: disciplinas, horários, salas e monitores responsáveis. Os alunos poderão se inscrever diretamente.

### Gestão de Monitores
O monitor poderá se candidatar a vagas de monitoria, definir disponibilidade de horários, registrar presença e notificar ausência. O sistema também validará os requisitos de CR para aprovação da candidatura.

### Indicação de Professores
Professores poderão recomendar alunos para vagas de monitoria por meio de um formulário digital, enviando a indicação ao coordenador.

### Dashboard do Coordenador
O coordenador terá acesso a um painel de controle com visão geral das disciplinas, escalas de horário, relatórios de horas dos monitores e estatísticas de participação.

### Notificações Automáticas
O sistema enviará lembretes para alunos e monitores 24h e 1h antes de cada monitoria agendada, a fim de reduzir faltas e esquecimentos.

### Relatórios e Estatísticas
O sistema fornecerá relatórios para coordenadores e professores, com dados sobre frequência dos alunos, desempenho dos monitores e indicadores de efetividade das monitorias.

## Referências Bibliográficas
- RATIONAL UNIFIED PROCESS. *Vision Document Template*. IBM, 2003. Disponível em: https://www.ibm.com/docs/en/rup/9.0. Acesso em: 22/09/2025.  
- BARBOSA, S. D. J; DA SILVA, B. S. *Interação Humano-Computador*. Elsevier, 2010.  
- Documento de visão da disciplina Projeto Back-End, Universidade IBMEC, 2025.

## Versionamento
| Data       | Versão | Descrição               | Autor(es)                       |
|-----------|--------|------------------------|--------------------------------|
| 22/09/2025 | 1.0    | Criação do documento    | João, Bernardo, Andreson, Gabriel |
