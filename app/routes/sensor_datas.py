from typing import Any

from bson import ObjectId
from fastapi import APIRouter, HTTPException, status
from pymongo.errors import PyMongoError

from app.database import get_sensor_collection
from app.models import SensorDataCreate, SensorDataResponse, SensorDataUpdate

router = APIRouter(prefix="/api/SensorDatas", tags=["Sensor Data"])


def serialize_sensor_data(document: dict[str, Any]) -> SensorDataResponse:
    return SensorDataResponse(
        id=str(document["_id"]),
        deviceId=document["deviceId"],
        temperature=document["temperature"],
        humidity=document["humidity"],
        createdAt=document["createdAt"],
    )


def parse_object_id(id: str) -> ObjectId:
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Id khong hop le",
        )
    return ObjectId(id)


def database_error() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="Khong ket noi duoc MongoDB. Hay kiem tra MongoDB dang chay.",
    )


@router.get("", response_model=list[SensorDataResponse])
def get_sensor_data() -> list[SensorDataResponse]:
    try:
        documents = get_sensor_collection().find().sort("createdAt", -1)
        return [serialize_sensor_data(document) for document in documents]
    except PyMongoError as exc:
        raise database_error() from exc


@router.get("/{id}", response_model=SensorDataResponse)
def get_sensor_data_by_id(id: str) -> SensorDataResponse:
    object_id = parse_object_id(id)
    try:
        document = get_sensor_collection().find_one({"_id": object_id})
    except PyMongoError as exc:
        raise database_error() from exc

    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Khong tim thay du lieu")

    return serialize_sensor_data(document)


@router.post("", response_model=SensorDataResponse, status_code=status.HTTP_201_CREATED)
def post_sensor_data(sensor_data: SensorDataCreate) -> SensorDataResponse:
    document = sensor_data.model_dump()
    try:
        result = get_sensor_collection().insert_one(document)
        document["_id"] = result.inserted_id
    except PyMongoError as exc:
        raise database_error() from exc

    return serialize_sensor_data(document)


@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def put_sensor_data(id: str, sensor_data: SensorDataUpdate) -> None:
    object_id = parse_object_id(id)
    try:
        result = get_sensor_collection().replace_one(
            {"_id": object_id},
            sensor_data.model_dump(),
        )
    except PyMongoError as exc:
        raise database_error() from exc

    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Khong tim thay du lieu")


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sensor_data(id: str) -> None:
    object_id = parse_object_id(id)
    try:
        result = get_sensor_collection().delete_one({"_id": object_id})
    except PyMongoError as exc:
        raise database_error() from exc

    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Khong tim thay du lieu")
