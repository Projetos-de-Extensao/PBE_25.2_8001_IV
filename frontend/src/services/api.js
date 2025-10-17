import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para adicionar token de autenticação se necessário
api.interceptors.request.use(
  (config) => {
    // Adicione aqui lógica de token se necessário
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Serviços para cada entidade
export const tiposUsuarioService = {
  getAll: () => api.get('/tipos-usuario/'),
  getById: (id) => api.get(`/tipos-usuario/${id}/`),
  create: (data) => api.post('/tipos-usuario/', data),
  update: (id, data) => api.put(`/tipos-usuario/${id}/`, data),
  delete: (id) => api.delete(`/tipos-usuario/${id}/`),
};

export const cursosService = {
  getAll: () => api.get('/cursos/'),
  getById: (id) => api.get(`/cursos/${id}/`),
  create: (data) => api.post('/cursos/', data),
  update: (id, data) => api.put(`/cursos/${id}/`, data),
  delete: (id) => api.delete(`/cursos/${id}/`),
};

export const salasService = {
  getAll: () => api.get('/salas/'),
  getById: (id) => api.get(`/salas/${id}/`),
  create: (data) => api.post('/salas/', data),
  update: (id, data) => api.put(`/salas/${id}/`, data),
  delete: (id) => api.delete(`/salas/${id}/`),
};

export const usuariosService = {
  getAll: () => api.get('/usuarios/'),
  getById: (id) => api.get(`/usuarios/${id}/`),
  create: (data) => api.post('/usuarios/', data),
  update: (id, data) => api.put(`/usuarios/${id}/`, data),
  delete: (id) => api.delete(`/usuarios/${id}/`),
};

export const funcionariosService = {
  getAll: () => api.get('/funcionarios/'),
  getById: (id) => api.get(`/funcionarios/${id}/`),
  create: (data) => api.post('/funcionarios/', data),
  update: (id, data) => api.put(`/funcionarios/${id}/`, data),
  delete: (id) => api.delete(`/funcionarios/${id}/`),
};

export const alunosService = {
  getAll: () => api.get('/alunos/'),
  getById: (id) => api.get(`/alunos/${id}/`),
  create: (data) => api.post('/alunos/', data),
  update: (id, data) => api.put(`/alunos/${id}/`, data),
  delete: (id) => api.delete(`/alunos/${id}/`),
};

export const vagasService = {
  getAll: () => api.get('/vagas/'),
  getById: (id) => api.get(`/vagas/${id}/`),
  create: (data) => api.post('/vagas/', data),
  update: (id, data) => api.put(`/vagas/${id}/`, data),
  delete: (id) => api.delete(`/vagas/${id}/`),
};

export const turmasService = {
  getAll: () => api.get('/turmas/'),
  getById: (id) => api.get(`/turmas/${id}/`),
  create: (data) => api.post('/turmas/', data),
  update: (id, data) => api.put(`/turmas/${id}/`, data),
  delete: (id) => api.delete(`/turmas/${id}/`),
};

export const participacoesMonitoriaService = {
  getAll: () => api.get('/participacoes-monitoria/'),
  getById: (id) => api.get(`/participacoes-monitoria/${id}/`),
  create: (data) => api.post('/participacoes-monitoria/', data),
  update: (id, data) => api.put(`/participacoes-monitoria/${id}/`, data),
  delete: (id) => api.delete(`/participacoes-monitoria/${id}/`),
};

export const presencasService = {
  getAll: () => api.get('/presencas/'),
  getById: (id) => api.get(`/presencas/${id}/`),
  create: (data) => api.post('/presencas/', data),
  update: (id, data) => api.put(`/presencas/${id}/`, data),
  delete: (id) => api.delete(`/presencas/${id}/`),
};

export const inscricoesService = {
  getAll: () => api.get('/inscricoes/'),
  getById: (id) => api.get(`/inscricoes/${id}/`),
  create: (data) => api.post('/inscricoes/', data),
  update: (id, data) => api.put(`/inscricoes/${id}/`, data),
  delete: (id) => api.delete(`/inscricoes/${id}/`),
};

export default api;
