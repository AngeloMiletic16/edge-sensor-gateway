import asyncio

from edge_sensor_gateway.core.models import SensorInfo
from edge_sensor_gateway.sensors.temperature import TemperatureSensor
from edge_sensor_gateway.storage.memory import InMemoryStorage


class GatewayService:
    def __init__(self) -> None:
        self.storage = InMemoryStorage()

        sensor_info = SensorInfo(
            sensor_id="temp-001",
            name="Temperature Sensor 1",
            sensor_type="temperature",
            unit="C",
            interval_seconds=2.0,
        )

        self.sensor = TemperatureSensor(sensor_info)
        self.storage.set_sensors([sensor_info])

    async def collect_once(self) -> None:
        reading = await self.sensor.read()
        self.storage.save_reading(reading)

    async def run(self) -> None:
        while True:
            await self.collect_once()
            await asyncio.sleep(self.sensor.info.interval_seconds)