import { useState } from 'react';

import BookItem from './Componentes/BookItem/BookItem';
import MenuIcon from './Componentes/MenuIcon/MenuIcon';
import Logo from './Componentes/Logo/Logo';
import UserInfo from './Componentes/UserInfo/UserInfo';
import Banner from './Componentes/Banner/Banner';
import Footer from './Componentes/Footer/Footer';
import BooksSection from './Componentes/BooksSection/BooksSection';

import api from './api';

function App(){

    const [token, setToken] = useState();

    api.interceptors.request.use(async config => {

    if (token) {
        api.defaults.headers.authorization = `Token ${token}`;
    }

    return config;
    });

    return(
        <div>
        <header>
            <MenuIcon />
            <Logo />
            <UserInfo setToken={setToken} />
        </header>
        <Banner />
        <div className="books-section">
      <div className="books-row">
        <div className="book-item">
          <BookItem
            user="Anônimo"
            ulrImg="https://marketplace.canva.com/EAE4oJOnMh0/1/0/1003w/canva-capa-de-livro-de-suspense-O7z4yw4a5k8.jpg"
            titulo="O Segredo nas Sombras"
            autor="Delany Shannon"
            sinopse="Desde que se apaixonou por Pietr, um lobisomem russo, sua vida se misturou com uma complexa trama de poderes envolvendo a família do rapaz. Pietr e seus familiares são os últimos indivíduos de uma linhagem mutante que resultou de experimentos científicos promovidos durante a Guerra Fria."
          />
        </div>
        <div className="book-item">
          <BookItem
            user="Usuário 2"
            ulrImg="https://marketplace.canva.com/EAE4oJOnMh0/1/0/1003w/canva-capa-de-livro-de-suspense-O7z4yw4a5k8.jpg"
            titulo="Livro 2"
            autor="Autor 2"
            sinopse="Sinopse do Livro 2"
          />
        </div>
        <div className="book-item">
          <BookItem
            user="Anônimo"
            ulrImg="https://marketplace.canva.com/EAE4oJOnMh0/1/0/1003w/canva-capa-de-livro-de-suspense-O7z4yw4a5k8.jpg"
            titulo="Livro 3"
            autor="Autor 3"
            sinopse="Sinopse do Livro 3"
          />
        </div>
      </div>
      <div className="books-row">
        <div className="book-item">
          <BookItem
            user="Anônimo"
            ulrImg="https://marketplace.canva.com/EAE4oJOnMh0/1/0/1003w/canva-capa-de-livro-de-suspense-O7z4yw4a5k8.jpg"
            titulo="Livro 4"
            autor="Autor 4"
            sinopse="Sinopse do Livro 4"
          />
        </div>
        <div className="book-item">
          <BookItem
            user="Anônimo"
            ulrImg="https://marketplace.canva.com/EAE4oJOnMh0/1/0/1003w/canva-capa-de-livro-de-suspense-O7z4yw4a5k8.jpg"
            titulo="Livro 5"
            autor="Autor 5"
            sinopse="Sinopse do Livro 5"
          />
        </div>
        <div className="book-item">
          <BookItem
            user="Anônimo"
            ulrImg="https://marketplace.canva.com/EAE4oJOnMh0/1/0/1003w/canva-capa-de-livro-de-suspense-O7z4yw4a5k8.jpg"
            titulo="Livro 6"
            autor="Autor 6"
            sinopse="Sinopse do Livro 6"
          />
        </div>
      </div>
      <div className="books-row">
        <div className="book-item">
          <BookItem
            user="Anônimo"
            ulrImg="https://marketplace.canva.com/EAE4oJOnMh0/1/0/1003w/canva-capa-de-livro-de-suspense-O7z4yw4a5k8.jpg"
            titulo="Livro 7"
            autor="Autor 7"
            sinopse="Sinopse do Livro 7"
          />
        </div>
        <div className="book-item">
          <BookItem
            user="Anônimo"
            ulrImg="https://marketplace.canva.com/EAE4oJOnMh0/1/0/1003w/canva-capa-de-livro-de-suspense-O7z4yw4a5k8.jpg"
            titulo="Livro 8"
            autor="Autor 8"
            sinopse="Sinopse do Livro 8"
          />
        </div>
        <div className="book-item">
          <BookItem
            user="Anônimo"
            ulrImg="https://marketplace.canva.com/EAE4oJOnMh0/1/0/1003w/canva-capa-de-livro-de-suspense-O7z4yw4a5k8.jpg"
            titulo="Livro 9"
            autor="Autor 9"
            sinopse="Sinopse do Livro 9"
          />
        </div>
      </div>
    </div>
        <footer>
            <Footer />
        </footer>
        </div>
    )   
}

export default App