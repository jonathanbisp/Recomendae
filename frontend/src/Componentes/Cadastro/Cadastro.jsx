import React, { useState } from 'react';
import './Cadastro.css';
import api from '../../api';

async function verifica(credentials){
  return api.post("/api/users", credentials
    )
    .then((response) => console.log(response.data.user.token))
    .catch((err) => {console.error("ops! ocorreu um erro" + err);
     });
}

function Cadastro({ onClose, setToken }) {
  const [tipoConta, setTipoConta] = useState('leitor');
  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [confirmarSenha, setConfirmarSenha] = useState('');
  const [erroEmail, setErroEmail] = useState('');
  const [erroSenha, setErroSenha] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!tipoConta || !nome || !email || !senha || !confirmarSenha) {
      alert('Por favor, preencha todos os campos obrigatórios.');
      return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setErroEmail('Por favor, insira um email válido.');
      return;
    }

    if (senha !== confirmarSenha) {
      setErroSenha('As senhas não correspondem.');
      return;
    }

    if (senha.length < 3) {
      setErroSenha('A senha deve ter pelo menos 3 caracteres.');
      return;
    }

    const token = await verifica
    ({
        "user": {
          "email": email,
          "password": senha,
          "username": nome
        }
      })
    setToken('Token '+token);
  };

  return (
    <div className="create-account-screen">
      <form onSubmit={handleSubmit} className="create-account-form">
        <button id="cadastro-close-button" className="close-button" type="button" onClick={onClose}>
          X
        </button>
        <h2>Criar Conta</h2>
        <div className="form-group">
          <label htmlFor="nome">Nome</label>
          <input type="text" id="nome" value={nome} onChange={(e) => setNome(e.target.value)} placeholder="Nome" />
        </div>
        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Email"
          />
          {erroEmail && <p className="erro-mensagem">{erroEmail}</p>}
        </div>
        <div className="form-group">
          <label htmlFor="senha">Senha</label>
          <input
            type="password"
            id="senha"
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
            placeholder="Senha"
          />
        </div>
        <div className="form-group">
          <label htmlFor="confirmarSenha">Confirmar Senha</label>
          <input
            type="password"
            id="confirmarSenha"
            value={confirmarSenha}
            onChange={(e) => setConfirmarSenha(e.target.value)}
            placeholder="Confirmar Senha"
          />
          {erroSenha && <p className="erro-mensagem">{erroSenha}</p>}
        </div>
        <button type="submit">Criar Conta</button>
      </form>
    </div>
  );
}

export default Cadastro;
