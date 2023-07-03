from fastapi import FastAPI
from routes import user, book
from db.database import create_tables
from core.events import create_start_app_handler, create_stop_app_handler

def get_application() -> FastAPI:
    application = FastAPI()

    application.add_event_handler(
        "startup",
        create_start_app_handler(application),
    )
    application.add_event_handler(
        "shutdown",
        create_stop_app_handler(application),
    )
    application.include_router(user.router)
    application.include_router(book.router)

    return application


app = get_application()

@app.get("/")
async def home():
    return {"version": "0.0.2"}

create_tables()