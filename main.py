import logging
import os

import psycopg
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(
    title="SurveyGuard API",
    description="HTTP API сервиса анкетирования SurveyGuard.",
    version="0.2.0",
    openapi_tags=[
        {"name": "system", "description": "Служебные эндпоинты."},
    ],
)

TEAM_NAME = "Команда А"

logger = logging.getLogger("uvicorn.error")


class MessageResponse(BaseModel):
    message: str


class HealthResponse(BaseModel):
    status: str
    database: str


class VersionResponse(BaseModel):
    version: str
    team: str


@app.get("/", tags=["system"], summary="Приветствие", response_model=MessageResponse)
async def root():
    """Корневой эндпоинт."""
    return {"message": "Hello World"}


@app.get(
    "/health",
    tags=["system"],
    summary="Проверка состояния",
    response_model=HealthResponse,
)
def health_check():
    """Приложение работает и база данных отвечает на запрос."""
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "database": "DATABASE_URL is not set"},
        )
    try:
        with psycopg.connect(database_url, connect_timeout=3) as conn:
            conn.execute("SELECT 1")
    except psycopg.Error as exc:
        logger.warning("Health check: database is unavailable: %s", exc)
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "database": "unavailable"},
        )
    return {"status": "healthy", "database": "ok"}


@app.get(
    "/version",
    tags=["system"],
    summary="Версия приложения",
    response_model=VersionResponse,
)
async def version():
    """Версия приложения и команда-владелец."""
    return {"version": app.version, "team": TEAM_NAME}