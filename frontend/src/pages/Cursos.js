import React, { useState, useEffect } from 'react';
import { cursosService } from '../services/api';
import Header from '../components/Header';
import { FaBook, FaEdit, FaTrash, FaPlus } from 'react-icons/fa';
import './DataPages.css';

const Cursos = () => {
  const [cursos, setCursos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    nome: '',
    ativo: true
  });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const response = await cursosService.getAll();
      setCursos(response.data.results || response.data);
      setError(null);
    } catch (err) {
      setError('Erro ao carregar cursos: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingId) {
        await cursosService.update(editingId, formData);
      } else {
        await cursosService.create(formData);
      }
      fetchData();
      resetForm();
    } catch (err) {
      setError('Erro ao salvar curso: ' + err.message);
    }
  };

  const handleEdit = (curso) => {
    setFormData({
      nome: curso.nome,
      ativo: curso.ativo
    });
    setEditingId(curso.id);
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir este curso?')) {
      try {
        await cursosService.delete(id);
        fetchData();
      } catch (err) {
        setError('Erro ao excluir curso: ' + err.message);
      }
    }
  };

  const resetForm = () => {
    setFormData({
      nome: '',
      ativo: true
    });
    setEditingId(null);
    setShowForm(false);
  };

  if (loading) return <div className="page-container"><div className="loading">Carregando...</div></div>;

  return (
    <div className="page-container">
      <Header title="Gerenciar Cursos" icon={<FaBook />} />
      
      <div className="content-wrapper">
        <div className="page-header">
          <h1><FaBook /> Cursos</h1>
          <button 
            className="btn-primary"
            onClick={() => setShowForm(!showForm)}
          >
            <FaPlus /> {showForm ? 'Cancelar' : 'Novo Curso'}
          </button>
        </div>

        {error && <div className="error-message">{error}</div>}

        {showForm && (
          <div className="form-card">
            <h2>{editingId ? 'Editar Curso' : 'Novo Curso'}</h2>
            <form onSubmit={handleSubmit}>
              <div className="form-grid">
                <div className="form-group full-width">
                  <label>Nome do Curso:</label>
                  <input
                    type="text"
                    value={formData.nome}
                    onChange={(e) => setFormData({...formData, nome: e.target.value})}
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
          <h2>Lista de Cursos</h2>
          <div className="table-responsive">
            <table className="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Nome</th>
                  <th>Status</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {cursos.map(curso => (
                  <tr key={curso.id}>
                    <td>{curso.id}</td>
                    <td>{curso.nome}</td>
                    <td>
                      <span className={`badge ${curso.ativo ? 'badge-success' : 'badge-danger'}`}>
                        {curso.ativo ? 'Ativo' : 'Inativo'}
                      </span>
                    </td>
                    <td>
                      <div className="action-buttons">
                        <button 
                          className="btn-icon btn-edit"
                          onClick={() => handleEdit(curso)}
                          title="Editar"
                        >
                          <FaEdit />
                        </button>
                        <button 
                          className="btn-icon btn-delete"
                          onClick={() => handleDelete(curso.id)}
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

export default Cursos;
