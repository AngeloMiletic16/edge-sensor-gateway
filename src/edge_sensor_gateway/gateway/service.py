import asyncio

from edge_sensor_gateway.alarms.engine import AlarmEngine
from edge_sensor_gateway.core.models import SensorInfo
from edge_sensor_gateway.sensors.base import BaseSensor
from edge_sensor_gateway.sensors.distance import DistanceSensor
from edge_sensor_gateway.sensors.temperature import TemperatureSensor
from edge_sensor_gateway.sensors.vibration import VibrationSensor
from edge_sensor_gateway.storage.memory import InMemoryStorage


class GatewayService:
    def __init__(self) -> None:
        self.storage = InMemoryStorage()
        self.alarm_engine = AlarmEngine()
        self.sensors: list[BaseSensor] = self._create_sensors()

        self.storage.set_sensors([sensor.info for sensor in self.sensors])

    def _create_sensors(self) -> list[BaseSensor]:
        temperature_info = SensorInfo(
            sensor_id="temp-001",
            name="Temperature Sensor 1",
            sensor_type="temperature",
            unit="C",
            interval_seconds=2.0,
        )

        distance_info = SensorInfo(
            sensor_id="dist-001",
            name="Distance Sensor 1",
            sensor_type="distance",
            unit="mm",
            interval_seconds=3.0,
        )

        vibration_info = SensorInfo(
            sensor_id="vib-001",
            name="Vibration Sensor 1",
            sensor_type="vibration",
            unit="g",
            interval_seconds=4.0,
        )

        return [
            TemperatureSensor(temperature_info),
            DistanceSensor(distance_info),
            VibrationSensor(vibration_info),
        ]

    async def _run_sensor(self, sensor: BaseSensor) -> None:
        while True:
            reading = await sensor.read()
            self.storage.save_reading(reading)

            alarm = self.alarm_engine.evaluate(reading)
            if alarm is not None:
                self.storage.save_alarm(alarm)

            await asyncio.sleep(sensor.info.interval_seconds)

    async def run(self) -> None:
        tasks = [asyncio.create_task(self._run_sensor(sensor)) for sensor in self.sensors]
        await asyncio.gather(*tasks)