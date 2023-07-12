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

    // Essa função impede o sistema acuse erro ao carregar a página
    function carrega(){
        if(livros === undefined){
            // Se quiser pode formatar a tela de carregamento para que ela fique mais agradável
            return "Carregando"
        }
        return livros.map((livro) => <BookItem titulo={livro.title} autor={livro.author.username} ulrImg={livro.body} sinopse={livro.description} slug={livro.slug} />)
    }

  return (<div class="books-section">
    {carrega()}
  </div>);

}

export default BooksSection