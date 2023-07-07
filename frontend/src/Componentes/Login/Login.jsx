import React from 'react';
import { useState } from 'react';
import api from '../../api';
import './Login.css';

function Login({ onClose }) {
  const [email, setEmail] = useState()
  const [senha, setSenha] = useState()

  function login(){
    api
      .post("/api/users/login", 
        {
          "user": {
            "email": email,
            "password": senha
          }
        })
      .then((response) => console.log(response.user.token))
      .catch((err) => {
        console.error("ops! ocorreu um erro" + err);
      });
  }


  return (
    <div className="login-screen">
      <form className="login-form">
        <button id="login-close-button" className="close-button" type="button" onClick={onClose}>
          X
        </button>
        <h2>Login</h2>
        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input type="text" id="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
        </div>
        <div className="form-group">
          <label htmlFor="password">Senha</label>
          <input type="password" id="password" value={senha} onChange={(e) => setSenha(e.target.value)} placeholder="Senha" />
        </div>
        <button type="submit" onClickCapture={login}>Entrar</button>
      </form>
    </div>
  );
}

export default Login;
