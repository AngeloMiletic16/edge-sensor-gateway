import asyncio

from edge_sensor_gateway.alarms.engine import AlarmEngine
from edge_sensor_gateway.config import load_sensor_config
from edge_sensor_gateway.gateway.broadcaster import EventBroadcaster
from edge_sensor_gateway.sensors.base import BaseSensor
from edge_sensor_gateway.sensors.factory import create_sensor
from edge_sensor_gateway.storage.memory import InMemoryStorage


class GatewayService:
    def __init__(self) -> None:
        self.storage = InMemoryStorage()
        self.alarm_engine = AlarmEngine()
        self.broadcaster = EventBroadcaster()
        self.sensors: list[BaseSensor] = self._create_sensors()

        self.storage.set_sensors([sensor.info for sensor in self.sensors])

    def _create_sensors(self) -> list[BaseSensor]:
        sensor_infos = load_sensor_config()
        return [create_sensor(sensor_info) for sensor_info in sensor_infos]

    async def _run_sensor(self, sensor: BaseSensor) -> None:
        while True:
            reading = await sensor.read()
            self.storage.save_reading(reading)
            await self.broadcaster.broadcast_reading(reading)

            alarm = self.alarm_engine.evaluate(reading)
            if alarm is not None:
                self.storage.save_alarm(alarm)
                await self.broadcaster.broadcast_alarm(alarm)

            await asyncio.sleep(sensor.info.interval_seconds)

    async def run(self) -> None:
        tasks = [asyncio.create_task(self._run_sensor(sensor)) for sensor in self.sensors]
        await asyncio.gather(*tasks)