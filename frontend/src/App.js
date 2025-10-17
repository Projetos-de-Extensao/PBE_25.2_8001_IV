import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Home from './pages/Home';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Alunos from './pages/Alunos';
import Turmas from './pages/Turmas';
import Vagas from './pages/Vagas';
import Cursos from './pages/Cursos';
import Presencas from './pages/Presencas';
import './App.css';

// Componente para rotas protegidas
function ProtectedRoute({ children }) {
  const token = localStorage.getItem('access_token');
  return token ? children : <Navigate to="/login" replace />;
}

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          {/* Rota de Login (sem Sidebar) */}
          <Route path="/login" element={<Login />} />
          
          {/* Rotas protegidas (com Sidebar) */}
          <Route path="/*" element={
            <ProtectedRoute>
              <Sidebar />
              <div className="main-content">
                <Routes>
                  <Route path="/" element={<Home />} />
                  <Route path="/dashboard" element={<Dashboard />} />
                  <Route path="/alunos" element={<Alunos />} />
                  <Route path="/turmas" element={<Turmas />} />
                  <Route path="/vagas" element={<Vagas />} />
                  <Route path="/cursos" element={<Cursos />} />
                  <Route path="/presencas" element={<Presencas />} />
                </Routes>
              </div>
            </ProtectedRoute>
          } />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

