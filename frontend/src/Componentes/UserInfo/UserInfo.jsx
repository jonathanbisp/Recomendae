import React, { useState } from 'react';
import './UserInfo.css';
import Cadastro from '../Cadastro/Cadastro';
import Login from '../Login/Login';
import api from '../../api';

function UserInfo({setToken}) {
  const [mostrarCadastro, setMostrarCadastro] = useState(false);
  const [mostrarLogin, setMostrarLogin] = useState(false);
  const [nomeUsuario, setNomeUsuario] = useState('');

  const handleAbrirCadastro = () => {
    setMostrarCadastro(true);
    setMostrarLogin(false);
  };

  const handleFecharCadastro = () => {
    setMostrarCadastro(false);
  };

  const handleAbrirLogin = () => {
    setMostrarLogin(true);
    setMostrarCadastro(false);
  };

  const handleFecharLogin = () => {
    setMostrarLogin(false);
  };

  const handleCadastroSucesso = (nome) => {
    setNomeUsuario(nome);
    handleFecharCadastro();
  };

  return (
    <div className="user-info">
      <div className="login-options">
        {!nomeUsuario && (
          <>
            <span className="login" onClick={handleAbrirLogin}>
              Entrar
            </span>
            <span className="create-account" onClick={handleAbrirCadastro}>
              Criar Conta
            </span>
          </>
        )}
        {nomeUsuario && <span className="logged-in-user">{nomeUsuario}</span>}
      </div>
      {mostrarCadastro && (
        <div className="popup-container" onClick={handleFecharCadastro}>
          <div className="popup" onClick={(e) => e.stopPropagation()}>
            <Cadastro onClose={handleFecharCadastro} onCadastroSucesso={handleCadastroSucesso} setToken={setToken} handleFecharCadastro={handleFecharCadastro} setNomeUsuario={setNomeUsuario} />
          </div>
        </div>
      )}
      {mostrarLogin && (
        <div className="popup-container" onClick={handleFecharLogin}>
          <div className="popup" onClick={(e) => e.stopPropagation()}>
            <Login onClose={handleFecharLogin} setToken={setToken} setNomeUsuario={setNomeUsuario} handleFecharLogin={handleFecharLogin} />
          </div>
        </div>
      )}
    </div>
  );
}

export default UserInfo;
