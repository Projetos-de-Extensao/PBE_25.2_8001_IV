import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  FaHome, 
  FaUserGraduate, 
  FaChalkboardTeacher, 
  FaBriefcase, 
  FaBook, 
  FaClipboardCheck,
  FaBars,
  FaTimes,
  FaChartBar
} from 'react-icons/fa';
import { motion } from 'framer-motion';
import './Sidebar.css';

const Sidebar = () => {
  const [isOpen, setIsOpen] = useState(true);
  const location = useLocation();

  const menuItems = [
    { path: '/', icon: FaHome, label: 'Início' },
    { path: '/dashboard', icon: FaChartBar, label: 'Dashboard' },
    { path: '/alunos', icon: FaUserGraduate, label: 'Alunos' },
    { path: '/turmas', icon: FaChalkboardTeacher, label: 'Turmas' },
    { path: '/vagas', icon: FaBriefcase, label: 'Vagas' },
    { path: '/cursos', icon: FaBook, label: 'Cursos' },
    { path: '/presencas', icon: FaClipboardCheck, label: 'Presenças' },
  ];

  const toggleSidebar = () => {
    setIsOpen(!isOpen);
  };

  return (
    <>
      <motion.div 
        className={`sidebar ${isOpen ? 'open' : 'closed'}`}
        initial={{ x: -250 }}
        animate={{ x: 0 }}
        transition={{ duration: 0.3 }}
      >
        <div className="sidebar-header">
          <div className="logo-container">
            {isOpen && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.2 }}
              >
                <h2 className="logo-text">Plataforma Casa</h2>
                <p className="logo-subtitle">Sistema de Monitoria</p>
              </motion.div>
            )}
          </div>
          <button className="toggle-btn" onClick={toggleSidebar}>
            {isOpen ? <FaTimes /> : <FaBars />}
          </button>
        </div>

        <nav className="sidebar-nav">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`nav-item ${isActive ? 'active' : ''}`}
                title={!isOpen ? item.label : ''}
              >
                <Icon className="nav-icon" />
                {isOpen && (
                  <motion.span
                    className="nav-label"
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.2 }}
                  >
                    {item.label}
                  </motion.span>
                )}
              </Link>
            );
          })}
        </nav>

        <div className="sidebar-footer">
          {isOpen && (
            <motion.div
              className="user-info"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.3 }}
            >
              <div className="user-avatar">
                <FaUserGraduate />
              </div>
              <div className="user-details">
                <p className="user-name">Administrador</p>
                <p className="user-role">Sistema</p>
              </div>
            </motion.div>
          )}
        </div>
      </motion.div>

      <div className={`sidebar-overlay ${isOpen ? 'show' : ''}`} onClick={toggleSidebar}></div>
    </>
  );
};

export default Sidebar;
