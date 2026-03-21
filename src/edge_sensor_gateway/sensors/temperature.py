import random

from edge_sensor_gateway.core.models import SensorReading
from edge_sensor_gateway.sensors.base import BaseSensor


class TemperatureSensor(BaseSensor):
    async def read(self) -> SensorReading:
        value = round(random.uniform(18.0, 30.0), 2)

        return SensorReading(
            sensor_id=self.info.sensor_id,
            sensor_type=self.info.sensor_type,
            value=value,
            unit=self.info.unit,
            status="ok",
        )