from src.services.authentication import autentication

def teste_validar_username_em_uso():
    assert autentication.check_username_is_taken("UsersRepository", "admin") == True

def teste_validar_email_em_uso():
    assert autentication.check_email_is_taken("UsersRepository", "test@gmail.com") == True
