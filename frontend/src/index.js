import React from 'react';
import ReactDOM from 'react-dom/client';
import "./Componentes/index.css"

import BooksSection from './Componentes/BooksSection/BooksSection';
import MenuIcon from './Componentes/MenuIcon/MenuIcon';
import Logo from './Componentes/Logo/Logo';
import UserInfo from './Componentes/UserInfo/UserInfo';
import SearchBar from './Componentes/SearchBar/SearchBar';
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
    <SearchBar />
      <Banner />
      <BooksSection />
         {/* <div class="books-section">
          <BookItem titulo="Velozes e Furiosos" avaliacao='3' autor="Moroana Morais" ulrImg="https://marketplace.canva.com/EAE4oJOnMh0/1/0/1003w/canva-capa-de-livro-de-suspense-O7z4yw4a5k8.jpg" />
          <BookItem titulo="Título2" avaliacao='3' autor="Autor12" ulrImg="https://marketplace.canva.com/EAE4oJOnMh0/1/0/1003w/canva-capa-de-livro-de-suspense-O7z4yw4a5k8.jpg" />
          <BookItem titulo="Título2" avaliacao='3' autor="Autor12" ulrImg="https://marketplace.canva.com/EAE4oJOnMh0/1/0/1003w/canva-capa-de-livro-de-suspense-O7z4yw4a5k8.jpg" />
    </div> */}
    <footer>
      <Footer />  
    </footer>
  </React.StrictMode>
);
