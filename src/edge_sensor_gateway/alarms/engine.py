from uuid import uuid4

from edge_sensor_gateway.core.models import AlarmEvent, SensorReading


class AlarmEngine:
    def evaluate(self, reading: SensorReading) -> AlarmEvent | None:
        if reading.sensor_type == "temperature" and reading.value > 28.0:
            return AlarmEvent(
                alarm_id=str(uuid4()),
                sensor_id=reading.sensor_id,
                sensor_type=reading.sensor_type,
                severity="warning",
                message=f"High temperature detected: {reading.value} {reading.unit}",
            )

        if reading.sensor_type == "vibration" and reading.value > 4.0:
            return AlarmEvent(
                alarm_id=str(uuid4()),
                sensor_id=reading.sensor_id,
                sensor_type=reading.sensor_type,
                severity="warning",
                message=f"High vibration detected: {reading.value} {reading.unit}",
            )

        return None