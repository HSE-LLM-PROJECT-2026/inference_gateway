from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.config import Settings, get_settings


class GenericPayload(BaseModel):
    id: str | None = None
    name: str | None = None
    cluster_id: str | None = None
    deployment_id: str | None = None
    alias: str | None = None
    status: str | None = None
    data: dict[str, Any] = Field(default_factory=dict)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def service_payload(settings: Settings) -> dict[str, Any]:
    return {
        "service": settings.service_name,
        "role": settings.service_role,
        "title": settings.service_title,
        "description": settings.service_description,
        "split_enabled": settings.service_split_enabled,
        "updated_at": now_iso(),
    }


def payload_id(payload: GenericPayload | None) -> str:
    if payload and payload.id:
        return payload.id
    if payload and payload.name:
        return payload.name
    return str(uuid4())


settings = get_settings()
app = FastAPI(title=settings.service_title, version="0.1.0")
store: dict[str, dict[str, Any]] = {}


@app.get("/livez")
async def livez() -> dict[str, Any]:
    return {"status": "ok", **service_payload(settings)}


@app.get("/health")
async def health() -> dict[str, Any]:
    return {"status": "ok", **service_payload(settings)}


@app.get("/service-info")
async def service_info() -> dict[str, Any]:
    return {
        **service_payload(settings),
        "service_to_service_urls": settings.service_to_service_urls,
    }


def row(resource: str, item_id: str, payload: GenericPayload | None = None, **extra: Any) -> dict[str, Any]:
    data = payload.model_dump(mode="json") if payload else {}
    status_value = data.get("status") or extra.pop("status", "accepted")
    item = {
        "id": item_id,
        "resource": resource,
        "service": settings.service_name,
        "role": settings.service_role,
        "status": status_value,
        "updated_at": now_iso(),
        **extra,
    }
    for key, value in data.items():
        if key != "status" and value is not None:
            item[key] = value
    store[f"{resource}:{item_id}"] = item
    return item


@app.post("/v1/chat/completions")
async def chat_completions(payload: GenericPayload | None = None) -> Any:
    return row("v1", payload_id(payload), payload, operation="chat_completions")


@app.post("/v1/completions")
async def completions(payload: GenericPayload | None = None) -> Any:
    return row("v1", payload_id(payload), payload, operation="completions")


@app.post("/deployments/{deployment_id}/proxy/{upstream_path:path}")
async def proxy_deployment(deployment_id: str, upstream_path: str, payload: GenericPayload | None = None) -> Any:
    return row("deployments", deployment_id, payload, operation="proxy_deployment", upstream_path=upstream_path)


@app.post("/traffic-routes/{alias}/proxy/{upstream_path:path}")
async def proxy_route(alias: str, upstream_path: str, payload: GenericPayload | None = None) -> Any:
    return row("traffic_routes", alias, payload, operation="proxy_route", upstream_path=upstream_path)
