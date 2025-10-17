-- Criação das novas tabelas para o sistema de monitorias

-- Tabela de Horários Disponíveis
CREATE TABLE IF NOT EXISTS gestao_monitoria_horariodisponivel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    monitor_id INTEGER NOT NULL,
    turma_id INTEGER NOT NULL,
    dia_semana VARCHAR(20) NOT NULL,
    horario_inicio TIME NOT NULL,
    horario_fim TIME NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT 1,
    FOREIGN KEY (monitor_id) REFERENCES gestao_monitoria_aluno(usuario_ptr_id) ON DELETE CASCADE,
    FOREIGN KEY (turma_id) REFERENCES gestao_monitoria_turma(id) ON DELETE CASCADE
);

-- Tabela de Agendamentos de Monitoria
CREATE TABLE IF NOT EXISTS gestao_monitoria_agendamentomonitoria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id INTEGER NOT NULL,
    turma_id INTEGER NOT NULL,
    monitor_id INTEGER NOT NULL,
    data DATE NOT NULL,
    horario_inicio TIME NOT NULL,
    horario_fim TIME NOT NULL,
    assunto VARCHAR(200) NOT NULL,
    descricao TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'pendente',
    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (aluno_id) REFERENCES gestao_monitoria_aluno(usuario_ptr_id) ON DELETE CASCADE,
    FOREIGN KEY (turma_id) REFERENCES gestao_monitoria_turma(id) ON DELETE CASCADE,
    FOREIGN KEY (monitor_id) REFERENCES gestao_monitoria_aluno(usuario_ptr_id) ON DELETE CASCADE
);

-- Tabela de Submissão de Horas
CREATE TABLE IF NOT EXISTS gestao_monitoria_submissaohoras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    monitor_id INTEGER NOT NULL,
    turma_id INTEGER NOT NULL,
    mes_referencia DATE NOT NULL,
    total_horas DECIMAL(5, 2) NOT NULL,
    descricao_atividades TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pendente',
    aprovado_por_id INTEGER NULL,
    data_submissao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_aprovacao DATETIME NULL,
    observacoes TEXT,
    FOREIGN KEY (monitor_id) REFERENCES gestao_monitoria_aluno(usuario_ptr_id) ON DELETE CASCADE,
    FOREIGN KEY (turma_id) REFERENCES gestao_monitoria_turma(id) ON DELETE CASCADE,
    FOREIGN KEY (aprovado_por_id) REFERENCES gestao_monitoria_funcionario(usuario_ptr_id) ON DELETE SET NULL
);

-- Índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_horario_monitor ON gestao_monitoria_horariodisponivel(monitor_id);
CREATE INDEX IF NOT EXISTS idx_agendamento_aluno ON gestao_monitoria_agendamentomonitoria(aluno_id);
CREATE INDEX IF NOT EXISTS idx_agendamento_monitor ON gestao_monitoria_agendamentomonitoria(monitor_id);
CREATE INDEX IF NOT EXISTS idx_agendamento_data ON gestao_monitoria_agendamentomonitoria(data);
CREATE INDEX IF NOT EXISTS idx_submissao_monitor ON gestao_monitoria_submissaohoras(monitor_id);
CREATE INDEX IF NOT EXISTS idx_submissao_status ON gestao_monitoria_submissaohoras(status);
