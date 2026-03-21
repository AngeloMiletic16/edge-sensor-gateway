from abc import ABC, abstractmethod

from edge_sensor_gateway.core.models import SensorInfo, SensorReading


class BaseSensor(ABC):
    def __init__(self, info: SensorInfo) -> None:
        self.info = info

    @abstractmethod
    async def read(self) -> SensorReading:
        pass