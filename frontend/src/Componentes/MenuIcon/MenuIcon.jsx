import React, { useEffect, useRef, useState } from 'react';
import './MenuIcon.css';
import MenuLateral from '../MenuLateral/MenuLateral.jsx';

function MenuIcon() {
  const [barraTarefasVisivel, setBarraTarefasVisivel] = useState(false);
  const menuIconRef = useRef(null);

  useEffect(() => {
    const handleClickOutsideMenu = (event) => {
      if (!menuIconRef.current.contains(event.target)) {
        setBarraTarefasVisivel(false); // Oculta a barra de tarefas ao clicar fora do ícone de menu
      }
    };

    document.addEventListener('click', handleClickOutsideMenu);

    return () => {
      document.removeEventListener('click', handleClickOutsideMenu);
    };
  }, []);

  const toggleMenu = () => {
    setBarraTarefasVisivel(!barraTarefasVisivel); // Altera o estado da barra de tarefas ao clicar no ícone de menu
  };

  const fecharMenu = () => {
    setBarraTarefasVisivel(false); // Fecha a barra de tarefas
  };

  return (
    <div>
      <div className="menu-icon" ref={menuIconRef} onClick={toggleMenu}>
        &#9776;
      </div>
      {barraTarefasVisivel && (
        <MenuLateral isOpen={barraTarefasVisivel} onClose={fecharMenu} />
      )}
    </div>
  );
}

export default MenuIcon;
