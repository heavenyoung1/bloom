from fastapi import FastAPI
from contextlib import asynccontextmanager

from backend.api.v0.routes import auth
from backend.core.config import settings
from backend.core.dependencies import get_db_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP ---
    db = get_db_connection()
    print("✅ Application started")

    yield  # <--- приложение работает здесь

    # --- SHUTDOWN ---
    await db.dispose()
    print("✅ Application stopped")


app = FastAPI(
    title="Attorney CRM",
    version="1.0.0",
    lifespan=lifespan,  # <--- современный способ
)

# Роуты
app.include_router(auth.router)
