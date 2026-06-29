from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SensorDataCreate(BaseModel):
    deviceId: str = Field(..., min_length=1, examples=["DEVICE_001"])
    temperature: float = Field(..., examples=[30.5])
    humidity: float = Field(..., examples=[70.2])
    createdAt: datetime = Field(default_factory=datetime.now)


class SensorDataUpdate(SensorDataCreate):
    pass


class SensorDataResponse(SensorDataCreate):
    id: str

    model_config = ConfigDict(from_attributes=True)


class BodyData(BaseModel):
    deviceId: str = Field(..., min_length=1, examples=["DEVICE_001"])
    version: int = Field(..., ge=0, examples=[1])
