# SurveyGuard

Система анкетирования с автоматической фильтрацией аномалий: выбросов и вбросов в голосовании, активности ботов и недобросовестного заполнения (когда пользователь проставляет везде «1» или случайные значения). ML-сервис анализирует каждый ответ и помечает подозрительные, а результат виден в админ-панели.

## Команда

- Волков Михаил — Product Owner, Backend Developer
- Елизавета Тропина — ML Engineer
- Иван Савчук — Frontend Developer

## Стек технологий

**Backend**
- Python 3.11
- FastAPI
- PostgreSQL 16
- SQLAlchemy 2.0 + Alembic
- Redis (кэш, rate limiting)

**ML**
- Python 3.11
- scikit-learn (Isolation Forest, LOF)
- XGBoost / LightGBM
- pandas, NumPy, scipy
- FastAPI (отдельный сервис инференса)

**Frontend**
- React 19 + TypeScript
- Vite
- TailwindCSS
- React Hook Form + Zod
- SurveyJS

**Инфраструктура**
- Docker + docker-compose
- GitHub Actions
- pytest, vitest

## Архитектура

```
Frontend (React) ──▶ Backend API (FastAPI) ──▶ ML Service (FastAPI)
                            │                         │
                            ▼                         ▼
                     PostgreSQL 16            Model Store
                     + Redis                  (весов в git нет)
```

Backend и ML-сервис — отдельные приложения. Backend вызывает `POST /predict`, получает `{ is_anomaly, confidence, reason }` и сохраняет флаг вместе с ответом. Если ML недоступен, ответ пользователя всё равно сохраняется, а флаг уходит в статус `pending`.

## Статус

Проект в активной разработке. Идёт работа над MVP: базовое голосование, авторизация, первый набор правил фильтрации и обучение модели на синтетических данных.

## Запуск через Docker Compose

Нужно: Docker с Compose v2 или новее (`docker compose version` отвечает), свободный порт 8000.

1. Создать файл с переменными окружения из примера:

   ```bash
   cp .env.example .env            # Windows PowerShell: Copy-Item .env.example .env
   ```

   Открыть `.env` и заменить `changeme` на свой пароль базы (латинские буквы и цифры).

2. Поднять стек:

   ```bash
   docker compose up --build
   ```

3. Проверить — во втором окне терминала или в браузере: `http://localhost:8000/health` отвечает `{"status":"healthy","database":"ok"}`, `docker compose ps` показывает `db` в состоянии `healthy`.

4. Остановить: `Ctrl+C` или `docker compose down`. Удалить вместе с данными базы: `docker compose down -v`.

Порт 8000 занят — задайте в `.env` `APP_PORT=8001` и проверяйте `http://localhost:8001/health`.

## Локальная разработка без Docker

```bash
uv sync
uv run uvicorn main:app --reload
```

Базы в этом режиме нет: `/` отвечает `200`, `/health` — `503` с `{"status":"unhealthy","database":"DATABASE_URL is not set"}`.

## API

OpenAPI-документация генерируется FastAPI автоматически из кода приложения:

- `/docs` — Swagger UI (интерактивная документация)
- `/redoc` — ReDoc
- `/openapi.json` — OpenAPI-спецификация

| Метод | Путь | Описание |
| --- | --- | --- |
| GET | `/` | Приветствие |
| GET | `/health` | Проверка приложения и подключения к PostgreSQL |
| GET | `/version` | Версия приложения и команда-владелец |

`GET /health` возвращает `{"status":"healthy","database":"ok"}` при доступной базе и `503` — при недоступной.

## Структура репозитория

```
backend/        # FastAPI, бизнес-логика, БД
ml_service/     # feature engineering, модели, /predict
frontend/       # React + TS + Vite
compose.yaml
Dockerfile
.env.example
CONTRIBUTING.md
```

## Документация

- `CONTRIBUTING.md` — правила разработки, стиль кода, чек-лист перед PR.
- `docs/adr/` — ADR 001 и ADR 002.
- `docs/environment-schema.md` — схема окружения проекта.

## Лицензия

MIT. См. файл `LICENSE`.