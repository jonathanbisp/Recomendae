import React from 'react';
import './MenuLateral.css';

function MenuLateral({ isOpen, onClose }) {
  return (
    <div className={`menu ${isOpen ? 'active' : ''}`}>
      <ul>
        <li><a href="#">Página Inicial</a></li>
        <li><a href="#">Livros</a></li>
        <li><a href="#">Autores</a></li>
        <li><a href="#">Sobre</a></li>
        <li><a href="#">Contato</a></li>
      </ul>
      <aside>
        <span className="close-icon" onClick={onClose}>x</span>
      </aside>
    </div>
  );
}

export default MenuLateral;
