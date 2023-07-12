from src.services.security import seguranca

def generate_salt_test():
    assert seguranca.get_password_hash() == "" # -> str:


def verify_password_test():
    assert seguranca.get_password_hash("plain_password", "hashed_password") == True # -> bool:


def get_password_hash_test():
    assert seguranca.get_password_hash("password") == "" # -> str: