---
id: dt
title: Design Thinking
---

## **Design Thinking**

### **1. Capa**

- **Título do Projeto:** Sistema de Gestão de Monitorias IBMEC  
- **Nome da Equipe:** Projeto Back-End IV  
- **Data:** 22/09/2025  
- **Logo da Empresa/Organização (se aplicável)**

---

### **2. Introdução**

- **Contexto do Projeto:** Atualmente, o processo de agendamento e gestão de monitorias no IBMEC é manual, dependendo de planilhas.  
- **Objetivo:** Otimizar o agendamento de monitorias, melhorar a comunicação entre os envolvidos e fornecer dados para a melhoria contínua do programa.  
- **Público-Alvo:** Alunos, Monitores, Professores e Coordenadores do IBMEC.  
- **Escopo:** Todo o processo de monitorias do IBMEC, desde inscrições até relatórios e acompanhamento.

---

### **3. Fases do Design Thinking**

#### **3.1. Empatia**

- **Pesquisa:** Entrevistas com alunos e observação do processo atual.  
- **Insights:**  
  - **Alunos:** Não sabem a sala ou horário das monitorias.  
  - **Monitores:** Têm dificuldade em organizar suas disponibilidades.  
  - **CASAS:**  Gastam tempo excessivo com planilhas.  

- **Personas:**  
**Ana** – Aluna Ocupada: 19 anos, 3º período de Administração, estágio à tarde. **Frustração:** perda de tempo procurando monitorias.

**Carla** – Aluna Iniciante: 18 anos, 1º período de Direito, ainda não conhece bem a unidade. **Frustração:** confusão sobre horários e salas.

**Diego** – Aluno Estudioso: 20 anos, 4º período de Economia, busca monitorias que complementem seu aprendizado. **Frustração:** falta de informações detalhadas sobre cada monitoria.

---

#### **3.2. Definição**

- **Problema Central:** Como permitir que alunos encontrem as monitorias rapidamente, com informações claras sobre horários, salas e monitores?  
- **Pontos de Vista (POV):** Alunos precisam de uma maneira rápida e centralizada de localizar monitorias, pois seu tempo é limitado entre estudos e estágio.

---

#### **3.3. Ideação**

- **Brainstorming:** Sessão de brainstorming gerou requisitos BS01 a BS08, incluindo:  
  - Sistema de busca com filtros.  
  - Calendário visual de monitorias.  
  - Notificações automáticas para alunos e monitores.  
  - Dashboard para cada perfil.  
  - Processo de candidatura online para monitores.

- **Seleção de Ideias:** Priorizadas pelo impacto no usuário e viabilidade técnica:  

| Funcionalidade | Impacto | Esforço |
|----------------|---------|---------|
| Agendamento rápido de monitorias | Alto | Médio |
| Notificações automáticas | Alto | Baixo |
| Dashboard do coordenador | Médio | Médio |
| Processo de candidatura online | Alto | Médio |

- **Fluxos Essenciais:**  
  - **Aluno:** Busca por disciplina, visualização de horários em calendário. (BS01, BS02).  
  - **Monitor:** Candidatura online, definição de disponibilidade, registro de presença (BS03, BS04, BS05).  
  - **Coordenador:** Cadastrar disciplinas, aprovação de horas e relatórios (BS08).

---

#### **3.4. Prototipagem**

- **Descrição do Protótipo:** Wireframes de baixa fidelidade no Figma, focando no fluxo do aluno: login → busca de disciplina → agendamento → confirmação.  
- **Materiais Utilizados:** Figma, caneta e papel para sketches iniciais.  
- **Testes Realizados:** 5 alunos testaram os wireframes, fornecendo feedback sobre usabilidade e clareza.

---

#### **3.5. Teste**

- **Feedback dos Usuários:**  
  - Protótipo intuitivo, mas usuários pediram mais detalhes sobre horários e salas.  
- **Ajustes Realizados:**  
  - Inclusão de informações detalhadas nas telas de monitoria.  
- **Resultados Finais:**  
  - Usuários conseguem encontrar e agendar monitorias em menos de 5 minutos.  
  - Redução significativa de erros de agendamento e perda de tempo.

---

### **4. Conclusão**

- **Resultados Obtidos:**  
  - Centralização de informações.  
  - Redução do esforço administrativo.  
  - Melhor experiência para alunos e monitores.  

- **Próximos Passos:**  
  - Desenvolvimento de dashboard para professores e coordenadores.  
  - Implementação de notificações automáticas.  
  - Testes com mais usuários e criação de protótipos de alta fidelidade.

---

### **5. Referências**

- BARBOSA, S. D. J.; DA SILVA, B. S. *Interação Humano-Computador*. Elsevier, 2010.  
- RATIONAL UNIFIED PROCESS. *Vision Document Template*. IBM, 2003. Disponível em: https://www.ibm.com/docs/en/rup/9.0  
- Documento de visão da disciplina de Projeto Back-End, Universidade IBMEC, 2025.
