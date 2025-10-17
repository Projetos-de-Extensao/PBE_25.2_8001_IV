import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  FaUserGraduate, 
  FaChalkboardTeacher, 
  FaBriefcase, 
  FaBook,
  FaClipboardCheck,
  FaArrowUp,
  FaArrowDown,
  FaChartLine
} from 'react-icons/fa';
import { motion } from 'framer-motion';
import Header from '../components/Header';
import { 
  alunosService, 
  turmasService, 
  vagasService, 
  cursosService,
  presencasService 
} from '../services/api';
import './Home.css';

const Home = () => {
  const [stats, setStats] = useState({
    alunos: 0,
    turmas: 0,
    vagas: 0,
    cursos: 0,
    presencas: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const [alunosRes, turmasRes, vagasRes, cursosRes, presencasRes] = await Promise.all([
        alunosService.getAll(),
        turmasService.getAll(),
        vagasService.getAll(),
        cursosService.getAll(),
        presencasService.getAll()
      ]);

      setStats({
        alunos: (alunosRes.data.results || alunosRes.data).length,
        turmas: (turmasRes.data.results || turmasRes.data).length,
        vagas: (vagasRes.data.results || vagasRes.data).length,
        cursos: (cursosRes.data.results || cursosRes.data).length,
        presencas: (presencasRes.data.results || presencasRes.data).length
      });
    } catch (error) {
      console.error('Erro ao carregar estatísticas:', error);
    } finally {
      setLoading(false);
    }
  };

  const statsCards = [
    {
      title: 'Total de Alunos',
      value: stats.alunos,
      icon: FaUserGraduate,
      color: '#0066cc',
      bgColor: 'rgba(0, 102, 204, 0.1)',
      change: '+12%',
      changeType: 'up',
      link: '/alunos'
    },
    {
      title: 'Turmas Ativas',
      value: stats.turmas,
      icon: FaChalkboardTeacher,
      color: '#28a745',
      bgColor: 'rgba(40, 167, 69, 0.1)',
      change: '+8%',
      changeType: 'up',
      link: '/turmas'
    },
    {
      title: 'Vagas Disponíveis',
      value: stats.vagas,
      icon: FaBriefcase,
      color: '#ffc107',
      bgColor: 'rgba(255, 193, 7, 0.1)',
      change: '-3%',
      changeType: 'down',
      link: '/vagas'
    },
    {
      title: 'Cursos',
      value: stats.cursos,
      icon: FaBook,
      color: '#17a2b8',
      bgColor: 'rgba(23, 162, 184, 0.1)',
      change: '+5%',
      changeType: 'up',
      link: '/cursos'
    }
  ];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const cardVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        duration: 0.4
      }
    }
  };

  if (loading) {
    return (
      <div className="home-container">
        <Header title="Dashboard" subtitle="Visão geral do sistema" />
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Carregando dados...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="home-container">
      <Header title="Dashboard" subtitle="Visão geral do sistema de monitoria" />

      <div className="dashboard-content">
        <motion.div 
          className="stats-grid"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          {statsCards.map((stat, index) => {
            const Icon = stat.icon;
            const ChangeIcon = stat.changeType === 'up' ? FaArrowUp : FaArrowDown;
            
            return (
              <motion.div key={index} variants={cardVariants}>
                <Link to={stat.link} className="stat-card">
                  <div className="stat-card-header">
                    <div className="stat-icon-wrapper" style={{ backgroundColor: stat.bgColor }}>
                      <Icon style={{ color: stat.color }} />
                    </div>
                    <div className={`stat-change ${stat.changeType}`}>
                      <ChangeIcon />
                      <span>{stat.change}</span>
                    </div>
                  </div>
                  <div className="stat-card-body">
                    <h3 className="stat-title">{stat.title}</h3>
                    <p className="stat-value">{stat.value}</p>
                  </div>
                </Link>
              </motion.div>
            );
          })}
        </motion.div>

        <div className="dashboard-grid">
          <motion.div 
            className="dashboard-card"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
          >
            <div className="card-header-dash">
              <h3>Atividades Recentes</h3>
              <FaChartLine className="card-icon" />
            </div>
            <div className="card-content">
              <div className="activity-item">
                <div className="activity-icon success">
                  <FaUserGraduate />
                </div>
                <div className="activity-details">
                  <p className="activity-title">Novo aluno cadastrado</p>
                  <p className="activity-time">Há 2 horas</p>
                </div>
              </div>
              <div className="activity-item">
                <div className="activity-icon info">
                  <FaChalkboardTeacher />
                </div>
                <div className="activity-details">
                  <p className="activity-title">Turma atualizada</p>
                  <p className="activity-time">Há 5 horas</p>
                </div>
              </div>
              <div className="activity-item">
                <div className="activity-icon warning">
                  <FaBriefcase />
                </div>
                <div className="activity-details">
                  <p className="activity-title">Nova vaga criada</p>
                  <p className="activity-time">Há 1 dia</p>
                </div>
              </div>
            </div>
          </motion.div>

          <motion.div 
            className="dashboard-card"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
          >
            <div className="card-header-dash">
              <h3>Acesso Rápido</h3>
              <FaClipboardCheck className="card-icon" />
            </div>
            <div className="card-content">
              <Link to="/presencas" className="quick-link">
                <FaClipboardCheck />
                <span>Registrar Presença</span>
              </Link>
              <Link to="/alunos" className="quick-link">
                <FaUserGraduate />
                <span>Novo Aluno</span>
              </Link>
              <Link to="/turmas" className="quick-link">
                <FaChalkboardTeacher />
                <span>Nova Turma</span>
              </Link>
              <Link to="/vagas" className="quick-link">
                <FaBriefcase />
                <span>Nova Vaga</span>
              </Link>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default Home;
