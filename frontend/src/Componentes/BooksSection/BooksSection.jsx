import BookItem from "../BookItem/BookItem";
import { useState, useEffect } from "react";
import api from "../../api";

function BooksSection (){
    const[livros, setLivros] = useState()

    useEffect(() => {
        api
        .get("/api/books")
        .then((response) => setLivros(response.data.books))
        .catch((err) => {
            console.error("ops! ocorreu um erro" + err);
        });
    }, []);

    function carrega(){
        if(livros === undefined){
            return "Carregando"
        }
        return livros.map((livro) => <BookItem titulo={livro.title} autor={livro.author.username} ulrImg={livro.body} sinopse={livro.description} />)
    }

  return (<div class="books-section">
    {carrega()}
  </div>);

}

export default BooksSection