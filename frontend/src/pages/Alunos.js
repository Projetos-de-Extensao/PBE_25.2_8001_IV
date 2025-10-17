import React, { useState, useEffect } from 'react';
import { alunosService, cursosService, tiposUsuarioService } from '../services/api';
import Header from '../components/Header';
import { FaUserGraduate, FaPlus, FaEdit, FaTrash } from 'react-icons/fa';
import { motion } from 'framer-motion';
import './DataPages.css';

const Alunos = () => {
  const [alunos, setAlunos] = useState([]);
  const [cursos, setCursos] = useState([]);
  const [tiposUsuario, setTiposUsuario] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    nome: '',
    email: '',
    tipo_usuario: '',
    matricula: '',
    curso: '',
    data_ingresso: '',
    periodo: '',
    cr_geral: '',
    ativo: true
  });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [alunosRes, cursosRes, tiposRes] = await Promise.all([
        alunosService.getAll(),
        cursosService.getAll(),
        tiposUsuarioService.getAll()
      ]);
      setAlunos(alunosRes.data.results || alunosRes.data);
      setCursos(cursosRes.data.results || cursosRes.data);
      setTiposUsuario(tiposRes.data.results || tiposRes.data);
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
        await alunosService.update(editingId, formData);
      } else {
        await alunosService.create(formData);
      }
      fetchData();
      resetForm();
    } catch (err) {
      setError('Erro ao salvar aluno: ' + err.message);
    }
  };

  const handleEdit = (aluno) => {
    setFormData({
      nome: aluno.nome,
      email: aluno.email,
      tipo_usuario: aluno.tipo_usuario,
      matricula: aluno.matricula,
      curso: aluno.curso,
      data_ingresso: aluno.data_ingresso,
      periodo: aluno.periodo,
      cr_geral: aluno.cr_geral,
      ativo: aluno.ativo
    });
    setEditingId(aluno.id);
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir este aluno?')) {
      try {
        await alunosService.delete(id);
        fetchData();
      } catch (err) {
        setError('Erro ao excluir aluno: ' + err.message);
      }
    }
  };

  const resetForm = () => {
    setFormData({
      nome: '',
      email: '',
      tipo_usuario: '',
      matricula: '',
      curso: '',
      data_ingresso: '',
      periodo: '',
      cr_geral: '',
      ativo: true
    });
    setEditingId(null);
    setShowForm(false);
  };

  if (loading) {
    return (
      <div className="page-container">
        <Header title="Alunos" subtitle="Gerenciamento de alunos" />
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Carregando alunos...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="page-container">
      <Header title="Alunos" subtitle={`${alunos.length} alunos cadastrados`} />

      <div className="page-content">
        <div className="content-header">
          <div className="header-info">
            <FaUserGraduate className="page-icon" />
            <h2>Lista de Alunos</h2>
          </div>
          <button 
            className="btn btn-primary"
            onClick={() => setShowForm(!showForm)}
          >
            <FaPlus />
            {showForm ? 'Cancelar' : 'Novo Aluno'}
          </button>
        </div>

        {error && <div className="error-message">{error}</div>}

        {showForm && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="form-card"
          >
            <h3 className="form-title">
              {editingId ? 'Editar Aluno' : 'Novo Aluno'}
            </h3>
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
                  <label>Email:</label>
                  <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({...formData, email: e.target.value})}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Matrícula:</label>
                  <input
                    type="text"
                    value={formData.matricula}
                    onChange={(e) => setFormData({...formData, matricula: e.target.value})}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Tipo de Usuário:</label>
                  <select
                    value={formData.tipo_usuario}
                    onChange={(e) => setFormData({...formData, tipo_usuario: e.target.value})}
                    required
                  >
                    <option value="">Selecione...</option>
                    {tiposUsuario.map(tipo => (
                      <option key={tipo.id} value={tipo.id}>{tipo.tipo}</option>
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
                  <label>Data de Ingresso:</label>
                  <input
                    type="date"
                    value={formData.data_ingresso}
                    onChange={(e) => setFormData({...formData, data_ingresso: e.target.value})}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Período:</label>
                  <input
                    type="number"
                    value={formData.periodo}
                    onChange={(e) => setFormData({...formData, periodo: e.target.value})}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>CR Geral:</label>
                  <input
                    type="number"
                    step="0.01"
                    value={formData.cr_geral}
                    onChange={(e) => setFormData({...formData, cr_geral: e.target.value})}
                    required
                  />
                </div>
              </div>

              <div className="form-actions">
                <button type="submit" className="btn btn-success">
                  {editingId ? 'Atualizar' : 'Cadastrar'}
                </button>
                <button type="button" className="btn btn-secondary" onClick={resetForm}>
                  Cancelar
                </button>
              </div>
            </form>
          </motion.div>
        )}

        <div className="table-card">
          <div className="table-wrapper">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Matrícula</th>
                  <th>Nome</th>
                  <th>Email</th>
                  <th>Curso</th>
                  <th>Período</th>
                  <th>CR</th>
                  <th>Status</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {alunos.map(aluno => (
                  <motion.tr
                    key={aluno.id}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.3 }}
                  >
                    <td className="font-weight-bold">{aluno.matricula}</td>
                    <td>{aluno.nome}</td>
                    <td>{aluno.email}</td>
                    <td>{aluno.curso_nome}</td>
                    <td>{aluno.periodo}º</td>
                    <td>{aluno.cr_geral}</td>
                    <td>
                      <span className={`badge ${aluno.ativo ? 'badge-success' : 'badge-danger'}`}>
                        {aluno.ativo ? 'Ativo' : 'Inativo'}
                      </span>
                    </td>
                    <td>
                      <div className="action-buttons">
                        <button 
                          className="btn-icon btn-edit"
                          onClick={() => handleEdit(aluno)}
                          title="Editar"
                        >
                          <FaEdit />
                        </button>
                        <button 
                          className="btn-icon btn-delete"
                          onClick={() => handleDelete(aluno.id)}
                          title="Excluir"
                        >
                          <FaTrash />
                        </button>
                      </div>
                    </td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Alunos;

