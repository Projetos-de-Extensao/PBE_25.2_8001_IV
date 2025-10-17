import React, { useState, useEffect } from 'react';
import { vagasService, cursosService, funcionariosService } from '../services/api';
import Header from '../components/Header';
import { FaBriefcase, FaEdit, FaTrash, FaPlus } from 'react-icons/fa';
import './DataPages.css';

const Vagas = () => {
  const [vagas, setVagas] = useState([]);
  const [cursos, setCursos] = useState([]);
  const [funcionarios, setFuncionarios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    nome: '',
    curso: '',
    coordenador: '',
    descricao: '',
    requisitos: '',
    ativo: true
  });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [vagasRes, cursosRes, funcRes] = await Promise.all([
        vagasService.getAll(),
        cursosService.getAll(),
        funcionariosService.getAll()
      ]);
      setVagas(vagasRes.data.results || vagasRes.data);
      setCursos(cursosRes.data.results || cursosRes.data);
      setFuncionarios(funcRes.data.results || funcRes.data);
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
        await vagasService.update(editingId, formData);
      } else {
        await vagasService.create(formData);
      }
      fetchData();
      resetForm();
    } catch (err) {
      setError('Erro ao salvar vaga: ' + err.message);
    }
  };

  const handleEdit = (vaga) => {
    setFormData({
      nome: vaga.nome,
      curso: vaga.curso,
      coordenador: vaga.coordenador,
      descricao: vaga.descricao,
      requisitos: vaga.requisitos,
      ativo: vaga.ativo
    });
    setEditingId(vaga.id);
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir esta vaga?')) {
      try {
        await vagasService.delete(id);
        fetchData();
      } catch (err) {
        setError('Erro ao excluir vaga: ' + err.message);
      }
    }
  };

  const resetForm = () => {
    setFormData({
      nome: '',
      curso: '',
      coordenador: '',
      descricao: '',
      requisitos: '',
      ativo: true
    });
    setEditingId(null);
    setShowForm(false);
  };

  if (loading) return <div className="page-container"><div className="loading">Carregando...</div></div>;

  return (
    <div className="page-container">
      <Header title="Gerenciar Vagas de Monitoria" icon={<FaBriefcase />} />
      
      <div className="content-wrapper">
        <div className="page-header">
          <h1><FaBriefcase /> Vagas de Monitoria</h1>
          <button 
            className="btn-primary"
            onClick={() => setShowForm(!showForm)}
          >
            <FaPlus /> {showForm ? 'Cancelar' : 'Nova Vaga'}
          </button>
        </div>

        {error && <div className="error-message">{error}</div>}

        {showForm && (
          <div className="form-card">
            <h2>{editingId ? 'Editar Vaga' : 'Nova Vaga'}</h2>
            <form onSubmit={handleSubmit}>
              <div className="form-grid">
                <div className="form-group">
                  <label>Nome da Vaga:</label>
                  <input
                    type="text"
                    value={formData.nome}
                    onChange={(e) => setFormData({...formData, nome: e.target.value})}
                    required
                  />
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
                  <label>Coordenador:</label>
                  <select
                    value={formData.coordenador}
                    onChange={(e) => setFormData({...formData, coordenador: e.target.value})}
                    required
                  >
                    <option value="">Selecione...</option>
                    {funcionarios.filter(f => f.coordenador).map(func => (
                      <option key={func.id} value={func.id}>{func.nome}</option>
                    ))}
                  </select>
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

                <div className="form-group full-width">
                  <label>Requisitos:</label>
                  <textarea
                    value={formData.requisitos}
                    onChange={(e) => setFormData({...formData, requisitos: e.target.value})}
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
          <h2>Lista de Vagas</h2>
          <div className="table-responsive">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Nome</th>
                  <th>Curso</th>
                  <th>Coordenador</th>
                  <th>Descrição</th>
                  <th>Status</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {vagas.map(vaga => (
                  <tr key={vaga.id}>
                    <td>{vaga.nome}</td>
                    <td>{vaga.curso_nome}</td>
                    <td>{vaga.coordenador_nome}</td>
                    <td>{vaga.descricao.substring(0, 50)}...</td>
                    <td>
                      <span className={`badge ${vaga.ativo ? 'badge-success' : 'badge-danger'}`}>
                        {vaga.ativo ? 'Ativa' : 'Inativa'}
                      </span>
                    </td>
                    <td>
                      <div className="action-buttons">
                        <button 
                          className="btn-icon btn-edit"
                          onClick={() => handleEdit(vaga)}
                          title="Editar"
                        >
                          <FaEdit />
                        </button>
                        <button 
                          className="btn-icon btn-delete"
                          onClick={() => handleDelete(vaga.id)}
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

export default Vagas;
