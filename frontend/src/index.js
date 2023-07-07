import React from 'react';
import ReactDOM from 'react-dom/client';
import "./Componentes/index.css"

import BooksSection from './Componentes/BooksSection/BooksSection';
import MenuIcon from './Componentes/MenuIcon/MenuIcon';
import Logo from './Componentes/Logo/Logo';
import UserInfo from './Componentes/UserInfo/UserInfo';
import Banner from './Componentes/Banner/Banner';
import Footer from './Componentes/Footer/Footer';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <header>
      <MenuIcon />
      <Logo />
      <UserInfo />
    </header>
      <Banner />
      <BooksSection />
    <footer>
      <Footer />  
    </footer>
  </React.StrictMode>
);
