from pydantic import BaseModel
from sqlalchemy import Column, Integer, String


class Usuario:
    __tablename__ = "Usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

class Autor(BaseModel):
    idAutor: int
    nome: str
    idGenero: int

class Livro(BaseModel):
    idLivro: int
    titulo: str
    idAutor: int
    idGenero: int

class Avaliacao(BaseModel):
    idAval: int
    idUsuario: int
    idLivro: int
    nota: float

class Genero(BaseModel):
    idGenero: int
    nome: str