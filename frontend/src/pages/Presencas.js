import React, { useState, useEffect } from 'react';
import { presencasService, turmasService, alunosService } from '../services/api';
import Header from '../components/Header';
import { FaClipboardCheck, FaEdit, FaTrash, FaPlus } from 'react-icons/fa';
import './DataPages.css';

const Presencas = () => {
  const [presencas, setPresencas] = useState([]);
  const [turmas, setTurmas] = useState([]);
  const [alunos, setAlunos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    turma: '',
    aluno: '',
    data: '',
    presente: false
  });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [presencasRes, turmasRes, alunosRes] = await Promise.all([
        presencasService.getAll(),
        turmasService.getAll(),
        alunosService.getAll()
      ]);
      setPresencas(presencasRes.data.results || presencasRes.data);
      setTurmas(turmasRes.data.results || turmasRes.data);
      setAlunos(alunosRes.data.results || alunosRes.data);
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
        await presencasService.update(editingId, formData);
      } else {
        await presencasService.create(formData);
      }
      fetchData();
      resetForm();
    } catch (err) {
      setError('Erro ao salvar presença: ' + err.message);
    }
  };

  const handleEdit = (presenca) => {
    setFormData({
      turma: presenca.turma,
      aluno: presenca.aluno,
      data: presenca.data,
      presente: presenca.presente
    });
    setEditingId(presenca.id);
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir este registro?')) {
      try {
        await presencasService.delete(id);
        fetchData();
      } catch (err) {
        setError('Erro ao excluir presença: ' + err.message);
      }
    }
  };

  const resetForm = () => {
    setFormData({
      turma: '',
      aluno: '',
      data: '',
      presente: false
    });
    setEditingId(null);
    setShowForm(false);
  };

  if (loading) return <div className="page-container"><div className="loading">Carregando...</div></div>;

  return (
    <div className="page-container">
      <Header title="Controle de Presenças" icon={<FaClipboardCheck />} />
      
      <div className="content-wrapper">
        <div className="page-header">
          <h1><FaClipboardCheck /> Controle de Presenças</h1>
          <button 
            className="btn-primary"
            onClick={() => setShowForm(!showForm)}
          >
            <FaPlus /> {showForm ? 'Cancelar' : 'Registrar Presença'}
          </button>
        </div>

        {error && <div className="error-message">{error}</div>}

        {showForm && (
          <div className="form-card">
            <h2>{editingId ? 'Editar Presença' : 'Registrar Presença'}</h2>
            <form onSubmit={handleSubmit}>
              <div className="form-grid">
                <div className="form-group">
                  <label>Turma:</label>
                  <select
                    value={formData.turma}
                    onChange={(e) => setFormData({...formData, turma: e.target.value})}
                    required
                  >
                    <option value="">Selecione...</option>
                    {turmas.map(turma => (
                      <option key={turma.id} value={turma.id}>{turma.nome}</option>
                    ))}
                  </select>
                </div>

                <div className="form-group">
                  <label>Aluno:</label>
                  <select
                    value={formData.aluno}
                    onChange={(e) => setFormData({...formData, aluno: e.target.value})}
                    required
                  >
                    <option value="">Selecione...</option>
                    {alunos.map(aluno => (
                      <option key={aluno.id} value={aluno.id}>{aluno.nome}</option>
                    ))}
                  </select>
                </div>

                <div className="form-group">
                  <label>Data:</label>
                  <input
                    type="date"
                    value={formData.data}
                    onChange={(e) => setFormData({...formData, data: e.target.value})}
                    required
                  />
                </div>

                <div className="form-group">
                  <label className="checkbox-label">
                    <input
                      type="checkbox"
                      checked={formData.presente}
                      onChange={(e) => setFormData({...formData, presente: e.target.checked})}
                    />
                    <span>Presente</span>
                  </label>
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
          <h2>Lista de Presenças</h2>
          <div className="table-responsive">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Data</th>
                  <th>Aluno</th>
                  <th>Turma</th>
                  <th>Status</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {presencas.map(presenca => (
                  <tr key={presenca.id}>
                    <td>{new Date(presenca.data).toLocaleDateString('pt-BR')}</td>
                    <td>{presenca.aluno_nome}</td>
                    <td>{presenca.turma_nome}</td>
                    <td>
                      <span className={`badge ${presenca.presente ? 'badge-success' : 'badge-danger'}`}>
                        {presenca.presente ? 'Presente' : 'Ausente'}
                      </span>
                    </td>
                    <td>
                      <div className="action-buttons">
                        <button 
                          className="btn-icon btn-edit"
                          onClick={() => handleEdit(presenca)}
                          title="Editar"
                        >
                          <FaEdit />
                        </button>
                        <button 
                          className="btn-icon btn-delete"
                          onClick={() => handleDelete(presenca.id)}
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

export default Presencas;
