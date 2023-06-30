from fastapi import FastAPI
from routers import user, book

app = FastAPI()

@app.get("/")
async def home():
    return {"version": "0.0.2"}

app.include_router(user.router)
app.include_router(book.router)