from edge_sensor_gateway.api.websocket import ConnectionManager
from edge_sensor_gateway.core.models import AlarmEvent, SensorReading


class EventBroadcaster:
    def __init__(self) -> None:
        self.manager = ConnectionManager()

    async def broadcast_reading(self, reading: SensorReading) -> None:
        await self.manager.broadcast_json(
            {
                "event_type": "reading",
                "payload": reading.model_dump(mode="json"),
            }
        )

    async def broadcast_alarm(self, alarm: AlarmEvent) -> None:
        await self.manager.broadcast_json(
            {
                "event_type": "alarm",
                "payload": alarm.model_dump(mode="json"),
            }
        )