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

## Установка и запуск

(Будет добавлено позже — после стабилизации docker-compose и появления `.env.example` в основном репозитории.)

## Структура репозитория

```
backend/        # FastAPI, бизнес-логика, БД
ml_service/     # feature engineering, модели, /predict
frontend/       # React + TS + Vite
docker-compose.yml
openapi.yaml
CONTRIBUTING.md
```

## Документация

- `CONTRIBUTING.md` — правила разработки, стиль кода, чек-лист перед PR.
- `openapi.yaml` — спецификация HTTP API.

## Лицензия

MIT. См. файл `LICENSE`.