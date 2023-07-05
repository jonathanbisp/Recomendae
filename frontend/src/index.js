import React from 'react';
import ReactDOM from 'react-dom/client';
import "./Componentes/index.css"

import BookItem from './Componentes/BookItem/BookItem';
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
      <div class="books-section">
        <div class="book-row">
          <BookItem titulo="Velozes e Furiosos" avaliacao='3' autor="Moroana Morais" editora="FTD" ulrImg="https://marketplace.canva.com/EAE4oJOnMh0/1/0/1003w/canva-capa-de-livro-de-suspense-O7z4yw4a5k8.jpg" />
          <BookItem titulo="Título2" avaliacao='3' autor="Autor12" editora="Editora31" ulrImg="https://marketplace.canva.com/EAE4oJOnMh0/1/0/1003w/canva-capa-de-livro-de-suspense-O7z4yw4a5k8.jpg" />
          <BookItem titulo="Título2" avaliacao='3' autor="Autor12" editora="Editora31" ulrImg="https://marketplace.canva.com/EAE4oJOnMh0/1/0/1003w/canva-capa-de-livro-de-suspense-O7z4yw4a5k8.jpg" />
        </div>
        <div class="book-row">
          <BookItem titulo="Velozes e Furiosos" avaliacao='3' autor="Moroana Morais" editora="FTD" ulrImg="https://marketplace.canva.com/EAE4oJOnMh0/1/0/1003w/canva-capa-de-livro-de-suspense-O7z4yw4a5k8.jpg" />
          <BookItem titulo="Título2" avaliacao='3' autor="Autor12" editora="Editora31" ulrImg="https://marketplace.canva.com/EAE4oJOnMh0/1/0/1003w/canva-capa-de-livro-de-suspense-O7z4yw4a5k8.jpg" />
          <BookItem titulo="Título2" avaliacao='3' autor="Autor12" editora="Editora31" ulrImg="https://marketplace.canva.com/EAE4oJOnMh0/1/0/1003w/canva-capa-de-livro-de-suspense-O7z4yw4a5k8.jpg" />
        </div>
        <div class="book-row">
          <BookItem titulo="Velozes e Furiosos" avaliacao='3' autor="Moroana Morais" editora="FTD" ulrImg="https://marketplace.canva.com/EAE4oJOnMh0/1/0/1003w/canva-capa-de-livro-de-suspense-O7z4yw4a5k8.jpg" />
          <BookItem titulo="Título2" avaliacao='3' autor="Autor12" editora="Editora31" ulrImg="https://marketplace.canva.com/EAE4oJOnMh0/1/0/1003w/canva-capa-de-livro-de-suspense-O7z4yw4a5k8.jpg" />
         <BookItem titulo="Título2" avaliacao='3' autor="Autor12" editora="Editora31" ulrImg="https://marketplace.canva.com/EAE4oJOnMh0/1/0/1003w/canva-capa-de-livro-de-suspense-O7z4yw4a5k8.jpg" />
       </div>
    </div>
    <footer>
      <Footer />  
    </footer>
  </React.StrictMode>
);
