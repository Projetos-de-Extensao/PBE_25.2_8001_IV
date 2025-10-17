import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import { FaUsers, FaChalkboardTeacher, FaBook, FaBriefcase, FaChartLine, FaFileExport } from 'react-icons/fa';
import Header from '../components/Header';
import './Dashboard.css';
import api from '../services/api';

function Dashboard() {
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState(null);

  const COLORS = ['#002555', '#0066cc', '#4d94ff', '#80b3ff', '#b3d1ff'];

  useEffect(() => {
    // Verificar autenticação
    const token = localStorage.getItem('access_token');
    const userData = localStorage.getItem('user');
    
    if (!token) {
      navigate('/login');
      return;
    }

    if (userData) {
      setUser(JSON.parse(userData));
    }

    loadStats();
  }, [navigate]);

  const loadStats = async () => {
    try {
      const response = await api.get('/dashboard/stats/');
      setStats(response.data);
    } catch (error) {
      console.error('Erro ao carregar estatísticas:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async () => {
    try {
      const response = await api.get('/relatorios/exportar/?tipo=geral', {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `relatorio_${new Date().toISOString().split('T')[0]}.xlsx`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Erro ao exportar relatório:', error);
      alert('Erro ao exportar relatório');
    }
  };

  if (loading) {
    return (
      <div className="page-container">
        <Header title="Dashboard" icon={<FaChartLine />} />
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Carregando estatísticas...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="page-container">
      <Header title="Dashboard" icon={<FaChartLine />} />
      
      <div className="content-wrapper">
        <div className="dashboard-welcome">
          <h2>Bem-vindo, {user?.first_name || user?.username}!</h2>
          <button onClick={handleExport} className="btn-export">
            <FaFileExport /> Exportar Relatório Completo
          </button>
        </div>

        {/* Cards de Resumo */}
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon" style={{background: '#002555'}}>
              <FaUsers />
            </div>
            <div className="stat-info">
              <h3>{stats?.totais?.alunos || 0}</h3>
              <p>Total de Alunos</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon" style={{background: '#0066cc'}}>
              <FaChalkboardTeacher />
            </div>
            <div className="stat-info">
              <h3>{stats?.totais?.monitores || 0}</h3>
              <p>Monitores Ativos</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon" style={{background: '#4d94ff'}}>
              <FaBook />
            </div>
            <div className="stat-info">
              <h3>{stats?.totais?.turmas || 0}</h3>
              <p>Turmas Ativas</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon" style={{background: '#80b3ff'}}>
              <FaBriefcase />
            </div>
            <div className="stat-info">
              <h3>{stats?.totais?.vagas || 0}</h3>
              <p>Vagas Disponíveis</p>
            </div>
          </div>
        </div>

        {/* Gráficos */}
        <div className="charts-grid">
          {/* Gráfico de Inscrições por Mês */}
          <div className="chart-card">
            <h3>Inscrições em Monitorias (Últimos 6 Meses)</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={stats?.inscricoes_por_mes?.reverse() || []}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="mes" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="total" 
                  stroke="#002555" 
                  strokeWidth={2}
                  name="Inscrições"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Gráfico de Frequência */}
          <div className="chart-card">
            <h3>Taxa de Frequência</h3>
            <div className="frequency-display">
              <div className="frequency-circle">
                <span className="frequency-percent">{stats?.frequencia?.taxa || 0}%</span>
                <p>Frequência Geral</p>
              </div>
              <div className="frequency-details">
                <p><strong>{stats?.frequencia?.presencas_mes || 0}</strong> presenças registradas este mês</p>
              </div>
            </div>
          </div>

          {/* Gráfico de Presença por Turma */}
          <div className="chart-card full-width">
            <h3>Presenças e Faltas por Turma</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={stats?.presenca_por_turma || []}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="turma" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="presencas" fill="#002555" name="Presenças" />
                <Bar dataKey="faltas" fill="#ff4444" name="Faltas" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Gráfico de Vagas Populares */}
          <div className="chart-card">
            <h3>Vagas Mais Procuradas</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={stats?.vagas_populares || []}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({nome, monitores}) => `${nome}: ${monitores}`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="monitores"
                >
                  {(stats?.vagas_populares || []).map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
