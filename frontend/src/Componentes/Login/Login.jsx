import React from 'react';
import { useState } from 'react';
import api from '../../api';
import './Login.css';

async function login(credentials){
  return api.post("/api/users/login", credentials
    )
    .then((response) => response.data.user.token)
    .catch((err) => {console.error("ops! ocorreu um erro" + err);
     });
}

function Login({ onClose, setToken }) {
  const [email, setEmail] = useState("")
  const [senha, setSenha] = useState("")

  const handleSubmit = async e => {
    e.preventDefault();
    const token = await login({
      "user": {
        "email": email,
        "password": senha
      }
    });
    setToken('Token '+token);
  }

  return (
    <div className="login-screen">
      <form className="login-form" onSubmit={handleSubmit}>
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
