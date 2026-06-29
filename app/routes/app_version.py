import os

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from app.models import BodyData

router = APIRouter(tags=["App Version"])


@router.get("/api/AppVersion", response_class=PlainTextResponse)
def get_app_version() -> str:
    return os.getenv("APP_VERSION", "Version 1.0")


@router.post("/api/PostVersion", response_class=PlainTextResponse)
def post_version(data: BodyData) -> str:
    print(f"DeviceId: {data.deviceId}")
    print(f"Version: {data.version}")
    return "Received"
