import os
from pathlib import Path

from celery.result import AsyncResult
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from worker import celery_app, send_notification

CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "*").split(",") if o.strip()]
FRONTEND_DIR = Path(os.getenv("FRONTEND_DIR", "/app/frontend"))

app = FastAPI(title="Notification Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


class NotifyRequest(BaseModel):
    message: str = "Hello from the DevOps assignment"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/notify/")
def notify(body: NotifyRequest | None = None):
    message = body.message if body else NotifyRequest().message
    task = send_notification.delay(message)
    return {"task_id": task.id, "status": "queued"}


@app.get("/task_status/{task_id}")
def task_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    payload = {"task_id": task_id, "status": result.status}
    if result.successful():
        payload["result"] = result.result
    elif result.failed():
        payload["result"] = str(result.result)
    else:
        payload["result"] = None
    return payload


@app.get("/")
def index():
    return FileResponse(FRONTEND_DIR / "index.html")
