from datetime import datetime, UTC
from pydantic import BaseModel, Field


class SensorReading(BaseModel):
    sensor_id: str
    sensor_type: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    value: float
    unit: str
    status: str = "ok"


class SensorInfo(BaseModel):
    sensor_id: str
    name: str
    sensor_type: str
    unit: str
    interval_seconds: float
    enabled: bool = True


class AlarmEvent(BaseModel):
    alarm_id: str
    sensor_id: str
    sensor_type: str
    severity: str
    message: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    active: bool = True


class HealthStatus(BaseModel):
    status: str
    active_sensors: int
    total_readings: int
    active_alarms: int