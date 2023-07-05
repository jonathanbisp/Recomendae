import React from 'react';
import './Login.css';

function Login({ onClose }) {
  return (
    <div className="login-screen">
      <form className="login-form">
        <button id="login-close-button" className="close-button" type="button" onClick={onClose}>
          X
        </button>
        <h2>Login</h2>
        <div className="form-group">
          <label htmlFor="username">Usuário</label>
          <input type="text" id="username" placeholder="Usuário" />
        </div>
        <div className="form-group">
          <label htmlFor="password">Senha</label>
          <input type="password" id="password" placeholder="Senha" />
        </div>
        <button type="submit">Entrar</button>
      </form>
    </div>
  );
}

export default Login;
