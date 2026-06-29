from fastapi import FastAPI

from app.routes import app_version, sensor_datas

app = FastAPI(
    title="Web API SensorData Demo",
    description="API demo tuong duong bai tap Web API, viet bang Python FastAPI va MongoDB.",
    version="1.0.0",
)

app.include_router(app_version.router)
app.include_router(sensor_datas.router)


@app.get("/", include_in_schema=False)
def root() -> dict[str, str]:
    return {"message": "Mo Swagger tai /docs"}
