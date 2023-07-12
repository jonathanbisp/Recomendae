from src.services.books import livros

def teste_validar_se_o_livro_existe():
    assert livros.check_book_exists("BooksRepository" "slug") == True # -> bool:

def test():
    assert livros.get_slug_for_book("title") == True # -> bool:

def teste_usuario_pode_modificar_o_livro():
    assert livros.check_user_can_modify_book("Book", "User") == True # -> bool:
