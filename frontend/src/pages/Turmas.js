import React, { useState, useEffect } from 'react';
import { turmasService, vagasService, salasService, alunosService, cursosService } from '../services/api';
import Header from '../components/Header';
import { FaUsers, FaEdit, FaTrash, FaPlus } from 'react-icons/fa';
import './DataPages.css';

const Turmas = () => {
  const [turmas, setTurmas] = useState([]);
  const [vagas, setVagas] = useState([]);
  const [salas, setSalas] = useState([]);
  const [alunos, setAlunos] = useState([]);
  const [cursos, setCursos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    nome: '',
    vaga: '',
    sala: '',
    descricao: '',
    data_inicio: '',
    data_fim: '',
    dias_da_semana: '',
    horario: '',
    monitor: '',
    curso: '',
    ativo: true
  });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [turmasRes, vagasRes, salasRes, alunosRes, cursosRes] = await Promise.all([
        turmasService.getAll(),
        vagasService.getAll(),
        salasService.getAll(),
        alunosService.getAll(),
        cursosService.getAll()
      ]);
      setTurmas(turmasRes.data.results || turmasRes.data);
      setVagas(vagasRes.data.results || vagasRes.data);
      setSalas(salasRes.data.results || salasRes.data);
      setAlunos(alunosRes.data.results || alunosRes.data);
      setCursos(cursosRes.data.results || cursosRes.data);
      setError(null);
    } catch (err) {
      setError('Erro ao carregar dados: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingId) {
        await turmasService.update(editingId, formData);
      } else {
        await turmasService.create(formData);
      }
      fetchData();
      resetForm();
    } catch (err) {
      setError('Erro ao salvar turma: ' + err.message);
    }
  };

  const handleEdit = (turma) => {
    setFormData({
      nome: turma.nome,
      vaga: turma.vaga,
      sala: turma.sala,
      descricao: turma.descricao,
      data_inicio: turma.data_inicio,
      data_fim: turma.data_fim,
      dias_da_semana: turma.dias_da_semana,
      horario: turma.horario,
      monitor: turma.monitor,
      curso: turma.curso,
      ativo: turma.ativo
    });
    setEditingId(turma.id);
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir esta turma?')) {
      try {
        await turmasService.delete(id);
        fetchData();
      } catch (err) {
        setError('Erro ao excluir turma: ' + err.message);
      }
    }
  };

  const resetForm = () => {
    setFormData({
      nome: '',
      vaga: '',
      sala: '',
      descricao: '',
      data_inicio: '',
      data_fim: '',
      dias_da_semana: '',
      horario: '',
      monitor: '',
      curso: '',
      ativo: true
    });
    setEditingId(null);
    setShowForm(false);
  };

  if (loading) return <div className="page-container"><div className="loading">Carregando...</div></div>;

  return (
    <div className="page-container">
      <Header title="Gerenciar Turmas" icon={<FaUsers />} />
      
      <div className="content-wrapper">
        <div className="page-header">
          <h1><FaUsers /> Turmas</h1>
          <button 
            className="btn-primary"
            onClick={() => setShowForm(!showForm)}
          >
            <FaPlus /> {showForm ? 'Cancelar' : 'Nova Turma'}
          </button>
        </div>

        {error && <div className="error-message">{error}</div>}

        {showForm && (
          <div className="form-card">
            <h2>{editingId ? 'Editar Turma' : 'Nova Turma'}</h2>
            <form onSubmit={handleSubmit}>
              <div className="form-grid">
                <div className="form-group">
                  <label>Nome:</label>
                  <input
                    type="text"
                    value={formData.nome}
                    onChange={(e) => setFormData({...formData, nome: e.target.value})}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Vaga:</label>
                  <select
                    value={formData.vaga}
                    onChange={(e) => setFormData({...formData, vaga: e.target.value})}
                    required
                  >
                    <option value="">Selecione...</option>
                    {vagas.map(vaga => (
                      <option key={vaga.id} value={vaga.id}>{vaga.nome}</option>
                    ))}
                  </select>
                </div>

                <div className="form-group">
                  <label>Sala:</label>
                  <select
                    value={formData.sala}
                    onChange={(e) => setFormData({...formData, sala: e.target.value})}
                    required
                  >
                    <option value="">Selecione...</option>
                    {salas.map(sala => (
                      <option key={sala.id} value={sala.id}>{sala.numero}</option>
                    ))}
                  </select>
                </div>

                <div className="form-group">
                  <label>Monitor:</label>
                  <select
                    value={formData.monitor}
                    onChange={(e) => setFormData({...formData, monitor: e.target.value})}
                    required
                  >
                    <option value="">Selecione...</option>
                    {alunos.map(aluno => (
                      <option key={aluno.id} value={aluno.id}>{aluno.nome}</option>
                    ))}
                  </select>
                </div>

                <div className="form-group">
                  <label>Curso:</label>
                  <select
                    value={formData.curso}
                    onChange={(e) => setFormData({...formData, curso: e.target.value})}
                    required
                  >
                    <option value="">Selecione...</option>
                    {cursos.map(curso => (
                      <option key={curso.id} value={curso.id}>{curso.nome}</option>
                    ))}
                  </select>
                </div>

                <div className="form-group">
                  <label>Data Início:</label>
                  <input
                    type="date"
                    value={formData.data_inicio}
                    onChange={(e) => setFormData({...formData, data_inicio: e.target.value})}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Data Fim:</label>
                  <input
                    type="date"
                    value={formData.data_fim}
                    onChange={(e) => setFormData({...formData, data_fim: e.target.value})}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Dias da Semana:</label>
                  <input
                    type="text"
                    placeholder="Ex: Segunda, Quarta, Sexta"
                    value={formData.dias_da_semana}
                    onChange={(e) => setFormData({...formData, dias_da_semana: e.target.value})}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Horário:</label>
                  <input
                    type="text"
                    placeholder="Ex: 18:00 - 21:00"
                    value={formData.horario}
                    onChange={(e) => setFormData({...formData, horario: e.target.value})}
                    required
                  />
                </div>

                <div className="form-group full-width">
                  <label>Descrição:</label>
                  <textarea
                    value={formData.descricao}
                    onChange={(e) => setFormData({...formData, descricao: e.target.value})}
                    rows="3"
                    required
                  />
                </div>
              </div>

              <div className="form-actions">
                <button type="submit" className="btn-primary">
                  {editingId ? 'Atualizar' : 'Cadastrar'}
                </button>
                <button type="button" className="btn-secondary" onClick={resetForm}>
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        )}

        <div className="table-card">
          <h2>Lista de Turmas</h2>
          <div className="table-responsive">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Nome</th>
                  <th>Curso</th>
                  <th>Monitor</th>
                  <th>Sala</th>
                  <th>Horário</th>
                  <th>Dias</th>
                  <th>Status</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {turmas.map(turma => (
                  <tr key={turma.id}>
                    <td>{turma.nome}</td>
                    <td>{turma.curso_nome}</td>
                    <td>{turma.monitor_nome}</td>
                    <td>{turma.sala_numero}</td>
                    <td>{turma.horario}</td>
                    <td>{turma.dias_da_semana}</td>
                    <td>
                      <span className={`badge ${turma.ativo ? 'badge-success' : 'badge-danger'}`}>
                        {turma.ativo ? 'Ativa' : 'Inativa'}
                      </span>
                    </td>
                    <td>
                      <div className="action-buttons">
                        <button 
                          className="btn-icon btn-edit"
                          onClick={() => handleEdit(turma)}
                          title="Editar"
                        >
                          <FaEdit />
                        </button>
                        <button 
                          className="btn-icon btn-delete"
                          onClick={() => handleDelete(turma.id)}
                          title="Excluir"
                        >
                          <FaTrash />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Turmas;
