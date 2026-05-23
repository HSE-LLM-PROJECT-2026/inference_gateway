# Inference Gateway

[HSE-LLM-PROJECT-2026/inference_gateway](https://github.com/HSE-LLM-PROJECT-2026/inference_gateway)

## Описание

FastAPI gateway для OpenAI-compatible инференса. В целевой архитектуре именно сюда приходят пользовательские запросы инференса, а сервис уже применяет маршрутизацию, квоты, учет стоимости и проверки доступа.

## Основные возможности

- OpenAI-compatible chat/completions endpoint
- proxy-запросы к конкретному deployment
- proxy-запросы через логический traffic route
- единая точка входа для клиентов инференса
- служебные health/livez/service-info ручки

## Основные API-ручки

- `/v1/chat/completions`
- `/v1/completions`
- `/deployments/{deployment_id}/proxy/{upstream_path}`
- `/traffic-routes/{alias}/proxy/{upstream_path}`

## Структура проекта

- `app/` — код FastAPI-сервиса
- `app/main.py` — HTTP API и базовая service runtime логика
- `app/config.py` — настройки сервиса через переменные окружения
- `deploy/` — файлы для раскатки сервиса
- `Dockerfile` — сборка контейнера
- `pyproject.toml`, `uv.lock` — зависимости Python
- `.env.example` — пример конфигурации

## Быстрый старт локально

1. Установить зависимости:
   ```bash
   uv sync --frozen
   ```

2. Запустить сервис:
   ```bash
   uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. Проверить, что сервис живой:
   ```bash
   curl http://localhost:8000/health
   ```

## Переменные окружения

- `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` — подключение к PostgreSQL
- `K8S_NAMESPACE` — namespace платформы в Kubernetes
- `SECURITY_AUDIT_BASE_URL` — адрес security/audit service
- `SECURITY_AUDIT_SERVICE_TOKEN` — service-to-service токен
- `STATUS_PROMETHEUS_BASE_URL` — адрес Prometheus для сервисов, которым нужны метрики
- `IMAGE_REPOSITORY`, `IMAGE_TAG`, `RELEASE_NAME`, `KUBECONFIG_PATH` — параметры deploy-скриптов

Полный пример лежит в `.env.example`.

## Docker

```bash
docker build -t awesomecosmonaut/inference_gateway:latest .
docker run --env-file .env -p 8000:8000 awesomecosmonaut/inference_gateway:latest
```

## Деплой

Файлы для раскатки лежат в `deploy/`.

```bash
cd deploy
./deploy-from-scratch.sh
```

Если нужно пересобрать образ и полностью переустановить сервис:

```bash
cd deploy
./rebuild-delete-deploy.sh
```

## Автор

Igor Malysh
