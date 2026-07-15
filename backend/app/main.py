from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import categories, exchange, health, items, stores, users
from app.config import settings
from app.infrastructure.database import engine, Base

app = FastAPI(title=settings.app_title, version=settings.app_version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items.router)
app.include_router(categories.router)
app.include_router(stores.router)
app.include_router(users.router)
app.include_router(exchange.router)
app.include_router(health.router)


@app.on_event("startup")
def on_startup():
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        print(f"[startup] DB connection failed: {e}")
