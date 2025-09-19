# Documento de Requisitos — Sistema de Controle de Trabalho dos Monitores (SCTM)

## 1. Introdução
### 1.1 Objetivo do documento
Este documento descreve os requisitos funcionais e não funcionais, regras de negócio, interfaces, restrições e critérios de aceitação para o **Sistema de Controle de Trabalho dos Monitores (SCTM)** da instituição. O público-alvo inclui stakeholders acadêmicos (coordenadores, diretores), equipes de desenvolvimento, QA e operadores do sistema.

### 1.2 Escopo do sistema
O SCTM gerencia cadastro de monitores, alocação de plantões/horários, registro de presença, registro de atividades realizadas, aprovações por coordenadores, acompanhamento de horas cumpridas por monitor, geração de relatórios, comunicação (notificações/e-mails) e exportação de dados para folha ou sistemas administrativos.

### 1.3 Definições importantes
- **Monitor**: estudante atribuído a atividades de apoio (aulas, plantões, laboratórios).
- **Coordenador**: responsável por validar escalas e horas.
- **Supervisor/Admin**: configurações do sistema, relatórios agregados e integração com APIs institucionais.
- **Plantão / Turno**: período em que o monitor atua.
- **Horas aprovadas**: horas que passaram por validação e contam para relatório/compensação.

---

## 2. Visão Geral do Sistema
### 2.1 Contexto
O SCTM ficará disponível como aplicação web responsiva (desktop e mobile) e será hospedado internamente ou na nuvem da instituição. Pode integrar-se ao sistema de autenticação da instituição (ex.: SSO/LDAP/SIGAA) e a sistemas administrativos para exportação de dados.

### 2.2 Principais funcionalidades
- Cadastro e gestão de usuários (monitores, coordenadores, administradores).
- Criação e publicação de vagas de monitoria.
- Escalonamento: criação de plantões/turnos e alocação de monitores.
- Check-in/check-out (registro de presença) e validação de horas.
- Registro de atividades e anexos (ata, fotos, logs).
- Workflow de aprovação de horas por coordenador.
- Painéis (dashboards) e relatórios (por monitor, disciplina, período).
- Notificações por e-mail e alertas no sistema.
- Exportação de dados (CSV / XLSX / PDF).
- Logs e auditoria de ações (quem editou/validou).

### 2.3 Restrições gerais
- Deve operar com navegadores modernos (Chrome, Firefox, Edge, Safari).
- Armazenamento de dados respeitando LGPD (quando aplicável).
- Integração com SSO pode ser opcional e depender de disponibilidade do serviço institucional.

---

## 3. Requisitos Funcionais (RF)
### Módulo: Autenticação e Controle de Acesso
- **RF001 — Cadastro de Usuário**: Cadastro de usuários com confirmação por e-mail.
- **RF002 — Autenticação (SSO / Local)**: Suporte a login institucional e local.
- **RF003 — Recuperação de Senha**: Recuperação de senha com link seguro.
- **RF004 — Perfis e Permissões**: Perfis (Administrador, Coordenador, Monitor, etc).

### Módulo: Gestão de Vagas e Escalas
- **RF010 — Criar Vaga de Monitoria**: Criação e publicação de vagas.
- **RF011 — Candidatura / Inscrição**: Inscrição de monitores em vagas.
- **RF012 — Alocação / Escala**: Criação de escalas evitando conflitos.

### Módulo: Registro de Presença e Atividades
- **RF020 — Check-in / Check-out**: Registro de presença com timestamps.
- **RF021 — Registro de Atividade**: Registro de atividades e anexos.
- **RF022 — Aprovação de Horas**: Aprovação/recusa por coordenador.

### Módulo: Relatórios e Dashboards
- **RF030 — Dashboard do Monitor**: Monitor visualiza horas e plantões.
- **RF031 — Relatório por Período**: Relatórios em CSV/XLSX/PDF.

### Módulo: Notificações e Comunicação
- **RF040 — Notificações**: Envio de notificações e e-mails.

### Módulo: Auditoria e Logs
- **RF050 — Log de Auditoria**: Registro de ações críticas.

---

## 4. Requisitos Não Funcionais (RNF)
- **RNF001 — Segurança**: Hash de senhas, TLS, proteção contra ataques comuns.
- **RNF002 — Privacidade (LGPD)**: Armazenamento mínimo de dados pessoais.
- **RNF003 — Performance**: Resposta média < 200ms em consultas simples.
- **RNF004 — Disponibilidade**: 99.5% em horário acadêmico.
- **RNF005 — Escalabilidade**: Suporte a aumento de usuários.
- **RNF006 — Usabilidade**: Interface intuitiva, acessibilidade WCAG AA.
- **RNF007 — Internacionalização**: Suporte inicial em português, preparado para tradução.
- **RNF008 — Backup e Recuperação**: Backups diários e retenção de 30 dias.

---

## 5. Regras de Negócio (RN)
- **RN01 — Unicidade de E-mail**: Cada usuário deve ter e-mail único.
- **RN02 — Validação de Matrícula**: Matrícula validada via sistema acadêmico.
- **RN03 — Limite de Horas**: Monitor não pode ultrapassar limite semanal.
- **RN04 — Aprovação Hierárquica**: Coordenador responsável deve aprovar horas.
- **RN05 — Prazos de Justificativa**: Recusas podem ser reapresentadas em até N dias.
- **RN06 — Política de Anexos**: Tipos e tamanhos permitidos definidos.
- **RN07 — Auditoria Obrigatória**: Alterações devem gerar log.
- **RN08 — Retenção de Dados**: Registros armazenados por pelo menos 2 anos.

---

## 6. Interfaces Externas
- **SSO/LDAP** para autenticação institucional.
- **Sistema Acadêmico** para validação de matrícula.
- **SMTP** para envio de e-mails.
- **Storage compatível com S3** para anexos e backups.
- **Exportação** em CSV/XLSX/PDF.

---

## 7. Restrições
- Sujeito às políticas de TI da instituição.
- Integração depende da disponibilidade de SSO/LDAP.
- Operação somente online.
- Limite de anexos e formatos.
- Conformidade com LGPD.

---

## 8. Critérios de Aceitação
- **CA-RF001**: Usuário criado, e-mail recebido, ativação bem-sucedida.
- **CA-RF020**: Check-in/out com timestamps corretos.
- **CA-RF022**: Aprovação/refusa gera notificação, soma correta de horas.
- **CA-RNF001**: Testes de segurança comprovam hash de senhas.
- **CA-Geral**: Documentação técnica e ambiente de staging entregues.

---

## 9. Glossário
- **SCTM**: Sistema de Controle de Trabalho dos Monitores.
- **SSO**: Single Sign-On.
- **LDAP**: Lightweight Directory Access Protocol.
- **LGPD**: Lei Geral de Proteção de Dados.
- **Plantão**: Período de monitoria.
- **CSV/XLSX**: Formatos de exportação.

---

## 10. Referências
- Políticas internas de TI da instituição.
- LGPD — Lei nº 13.709/2018.
- OWASP Top 10.
- RFC 8252 — OAuth 2.0 for Native Apps.
- Documentação da API acadêmica.
