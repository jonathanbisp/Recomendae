from src.services.reviews import reviews

def teste_usuario_pode_modificar_a_avaliação(Review, User):
    assert reviews.check_username_is_taken("UsersRepository", "admin") == True # -> bool: