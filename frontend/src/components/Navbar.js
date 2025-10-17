import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          Plataforma Casa
        </Link>
        <ul className="navbar-menu">
          <li className="navbar-item">
            <Link to="/" className="navbar-link">Home</Link>
          </li>
          <li className="navbar-item">
            <Link to="/alunos" className="navbar-link">Alunos</Link>
          </li>
          <li className="navbar-item">
            <Link to="/turmas" className="navbar-link">Turmas</Link>
          </li>
          <li className="navbar-item">
            <Link to="/vagas" className="navbar-link">Vagas</Link>
          </li>
          <li className="navbar-item">
            <Link to="/cursos" className="navbar-link">Cursos</Link>
          </li>
          <li className="navbar-item">
            <Link to="/presencas" className="navbar-link">Presenças</Link>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
