from edge_sensor_gateway.core.models import AlarmEvent, HealthStatus, SensorInfo, SensorReading


class InMemoryStorage:
    def __init__(self) -> None:
        self.sensors: list[SensorInfo] = []
        self.latest_readings: dict[str, SensorReading] = {}
        self.alarms: list[AlarmEvent] = []
        self.total_readings: int = 0

    def set_sensors(self, sensors: list[SensorInfo]) -> None:
        self.sensors = sensors

    def save_reading(self, reading: SensorReading) -> None:
        self.latest_readings[reading.sensor_id] = reading
        self.total_readings += 1

    def save_alarm(self, alarm: AlarmEvent) -> None:
        self.alarms.append(alarm)

    def get_sensors(self) -> list[SensorInfo]:
        return self.sensors

    def get_latest_readings(self) -> list[SensorReading]:
        return list(self.latest_readings.values())

    def get_alarms(self) -> list[AlarmEvent]:
        return self.alarms

    def get_health(self) -> HealthStatus:
        return HealthStatus(
            status="running",
            active_sensors=len(self.sensors),
            total_readings=self.total_readings,
            active_alarms=len(self.alarms),
        )