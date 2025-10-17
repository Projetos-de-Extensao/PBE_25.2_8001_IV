import React from 'react';
import { FaBell, FaSearch, FaUser } from 'react-icons/fa';
import './Header.css';

const Header = ({ title, subtitle }) => {
  return (
    <header className="app-header">
      <div className="header-left">
        <div className="header-title-section">
          <h1 className="header-title">{title || 'Dashboard'}</h1>
          {subtitle && <p className="header-subtitle">{subtitle}</p>}
        </div>
      </div>

      <div className="header-right">
        <div className="search-box">
          <FaSearch className="search-icon" />
          <input 
            type="text" 
            placeholder="Buscar..." 
            className="search-input"
          />
        </div>

        <button className="header-btn notification-btn">
          <FaBell />
          <span className="badge">3</span>
        </button>

        <div className="user-menu">
          <div className="user-avatar-header">
            <FaUser />
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
