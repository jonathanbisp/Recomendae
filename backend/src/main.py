from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from databases import database
from models import Usuario
from crud import get_user, create_user
from login import Hash

app = FastAPI()

security = HTTPBasic()

@app.get("/")
async def home():
    return {"version": "0.0.2"}

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    
@app.post("/cadastro")
async def cadastrar_usuario(user: Usuario, db: Session = Depends(database.get_connection)):
    db_user = get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Nome de usuário já existente")
    db_user = get_user(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Endereço de e-mail já cadastrado")
    new_user = Usuario(
        nome=user.nome,
        email=user.email,
        username=user.username,
        password=user.password,
    )
    create_user(db, new_user)
    return {"message": "Usuário cadastrado com sucesso!"}

@app.post("/login")
async def login(credentials: HTTPBasicCredentials, db: Session = Depends(database.get_connection)):
    user = get_user(db, username=credentials.username)
    if not user or not Hash.verify(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return {"message": "Login bem-sucedido!"}