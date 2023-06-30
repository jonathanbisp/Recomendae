from fastapi import FastAPI
from routers import user, book

app = FastAPI()

app.include_router(user.router)
app.include_router(book.router)