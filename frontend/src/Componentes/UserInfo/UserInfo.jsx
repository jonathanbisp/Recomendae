import React, { useState } from 'react';
import './UserInfo.css';
import Cadastro from '../Cadastro/Cadastro';

function UserInfo() {
  const [mostrarCadastro, setMostrarCadastro] = useState(false);
  const [nomeUsuario, setNomeUsuario] = useState('');
  
  const handleAbrirCadastro = () => {
    setMostrarCadastro(true);
  };

  const handleFecharCadastro = () => {
    setMostrarCadastro(false);
  };

  const handleCadastroSucesso = (nome) => {
    setNomeUsuario(nome);
  };

  return (
    <div className="user-info">
      <div className="login-options">
        {!nomeUsuario && (
          <>
            <span className="login">Entrar</span>
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
            <button className="close-button">X</button>
            <Cadastro onCadastroSucesso={handleCadastroSucesso} />
          </div>
        </div>
      )}
    </div>
  );
}

export default UserInfo;
