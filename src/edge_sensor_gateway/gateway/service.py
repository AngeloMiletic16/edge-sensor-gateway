import asyncio

from edge_sensor_gateway.alarms.engine import AlarmEngine
from edge_sensor_gateway.config import load_app_config
from edge_sensor_gateway.gateway.broadcaster import EventBroadcaster
from edge_sensor_gateway.mqtt.publisher import MqttPublisher
from edge_sensor_gateway.mqtt.topics import alarm_topic, gateway_health_topic, reading_topic
from edge_sensor_gateway.sensors.base import BaseSensor
from edge_sensor_gateway.sensors.factory import create_sensor
from edge_sensor_gateway.storage.memory import InMemoryStorage


class GatewayService:
    def __init__(self) -> None:
        self.storage = InMemoryStorage()
        self.alarm_engine = AlarmEngine()
        self.broadcaster = EventBroadcaster()

        self.app_config = load_app_config()
        self.mqtt_publisher = MqttPublisher(
            host=self.app_config.mqtt.host,
            port=self.app_config.mqtt.port,
            enabled=self.app_config.mqtt.enabled,
        )

        self.sensors: list[BaseSensor] = self._create_sensors()
        self.storage.set_sensors([sensor.info for sensor in self.sensors])

    def _create_sensors(self) -> list[BaseSensor]:
        return [create_sensor(sensor_info) for sensor_info in self.app_config.sensors]

    async def _run_sensor(self, sensor: BaseSensor) -> None:
        while True:
            reading = await sensor.read()
            self.storage.save_reading(reading)
            await self.broadcaster.broadcast_reading(reading)

            self.mqtt_publisher.publish(
                reading_topic(reading.sensor_id),
                reading.model_dump(mode="json"),
            )

            alarm = self.alarm_engine.evaluate(reading)
            if alarm is not None:
                self.storage.save_alarm(alarm)
                await self.broadcaster.broadcast_alarm(alarm)
                self.mqtt_publisher.publish(
                    alarm_topic(alarm.severity),
                    alarm.model_dump(mode="json"),
                )

            await asyncio.sleep(sensor.info.interval_seconds)

    async def _publish_health_loop(self) -> None:
        while True:
            health = self.storage.get_health()
            self.mqtt_publisher.publish(
                gateway_health_topic(),
                health.model_dump(mode="json"),
            )
            await asyncio.sleep(5)

    async def run(self) -> None:
        self.mqtt_publisher.connect()

        tasks = [asyncio.create_task(self._run_sensor(sensor)) for sensor in self.sensors]
        tasks.append(asyncio.create_task(self._publish_health_loop()))

        await asyncio.gather(*tasks)