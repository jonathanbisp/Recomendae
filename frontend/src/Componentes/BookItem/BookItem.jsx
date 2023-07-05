import "./BookItem.css";

function BookItem({ulrImg, titulo, avaliacao, autor, editora}){
    return(<div class="book-item">
    <img src={ulrImg} alt="Capa do Livro" />
    <div class="title">{titulo} </div>
    <div class="rating">&#9733;&#9733;&#9733;&#9734;&#9734;</div>
    <div>{autor}/{editora}</div>
  </div>)
}

export default BookItem
