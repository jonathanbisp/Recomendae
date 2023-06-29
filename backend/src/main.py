from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def home():
    return {"version": "0.0.2"}