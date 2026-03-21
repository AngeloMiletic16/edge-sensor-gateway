from fastapi import FastAPI

from edge_sensor_gateway.gateway.service import GatewayService

gateway_service = GatewayService()
app = FastAPI(title="Edge Sensor Gateway Simulator")


@app.on_event("startup")
async def startup_event() -> None:
    import asyncio
    asyncio.create_task(gateway_service.run())


@app.get("/")
async def root():
    return {"message": "Edge Sensor Gateway Simulator is running"}


@app.get("/health")
async def get_health():
    return gateway_service.storage.get_health()


@app.get("/sensors")
async def get_sensors():
    return gateway_service.storage.get_sensors()


@app.get("/readings/latest")
async def get_latest_readings():
    return gateway_service.storage.get_latest_readings()


@app.get("/alarms")
async def get_alarms():
    return gateway_service.storage.get_alarms()