# Inference Gateway

## Описание

Этот репозиторий содержит gateway для OpenAI-compatible инференса. Через него проходят запросы клиентов к моделям: сервис проверяет доступ, применяет квоты, выбирает маршрут и фиксирует стоимость запроса.

## Основные возможности
- OpenAI-compatible endpoint для chat/completions
- proxy-запросы к конкретному deployment
- proxy-запросы через traffic route
- проверка JWT или технического токена
- интеграция с quota service и cost service
- служебные health/livez/service-info ручки

## Структура проекта

- `app/` — основной код приложения
  - `main.py` — FastAPI-приложение и HTTP-ручки
  - `config.py` — настройки сервиса

- `deploy/` — файлы и переменные для развертывания
- `.env.example` — пример переменных окружения
- `Dockerfile` — сборка Docker-образа
- `pyproject.toml` — зависимости и настройки Python-проекта
- `requirements.txt` — список зависимостей для совместимого запуска без uv

## Быстрый старт локально

1. Установите зависимости:
   ```bash
   uv sync
   ```

2. Создайте `.env` на основе `.env.example`:
   ```bash
   cp .env.example .env
   ```

3. Запустите сервис:
   ```bash
   uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

Если `uv` не используется, можно запустить через обычный virtualenv:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Переменные окружения
- `ROUTING_SERVICE_URL`
- `QUOTA_SERVICE_URL`
- `COST_SERVICE_URL`
- `SECURITY_SERVICE_URL`
- `DEPLOYMENT_SERVICE_URL`
- `SERVICE_TOKEN`
- `REQUEST_TIMEOUT_SECONDS`
- `LOG_LEVEL`

Пример `.env`:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/llm_platform
SERVICE_TOKEN=change-me
LOG_LEVEL=INFO
```

## Основные API-ручки
- `GET /health`
- `GET /livez`
- `GET /service-info`
- `POST /v1/chat/completions`
- `POST /deployments/{deployment_id}/proxy/{path:path}`
- `POST /routes/{alias}/proxy/{path:path}`

## Сборка и запуск в Docker

```bash
docker build -t hse-llm-project-2026/inference_gateway:local .
docker run --env-file .env -p 8000:8000 hse-llm-project-2026/inference_gateway:local
```

## Деплой в Kubernetes

Файлы развертывания лежат в папке `deploy/`. Для сервисов, которые уже подключены к стенду, используются Helm values и deploy-скрипты из соответствующего репозитория или общего инфраструктурного пайплайна.

## Метрики и документация

- Swagger UI: `/docs`
- OpenAPI: `/openapi.json`
- Health check: `/health`
- Liveness check: `/livez`

## Автор

Igor Malysh
