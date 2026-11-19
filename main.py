from fastapi import FastAPI
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


class MessageResponse(BaseModel):
    message: str


class HealthResponse(BaseModel):
    status: str


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
async def health_check():
    """Проверка работоспособности сервиса."""
    return {"status": "healthy"}


@app.get(
    "/version",
    tags=["system"],
    summary="Версия приложения",
    response_model=VersionResponse,
)
async def version():
    """Версия приложения и команда-владелец."""
    return {"version": app.version, "team": TEAM_NAME}