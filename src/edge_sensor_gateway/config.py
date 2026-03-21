from pathlib import Path

import yaml
from pydantic import BaseModel

from edge_sensor_gateway.core.models import SensorInfo


class MqttConfig(BaseModel):
    enabled: bool = False
    host: str = "localhost"
    port: int = 1883


class AppConfig(BaseModel):
    sensors: list[SensorInfo]
    mqtt: MqttConfig


def load_app_config(config_path: str = "configs/sensors.example.yaml") -> AppConfig:
    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}

    sensors_data = data.get("sensors", [])
    mqtt_data = data.get("mqtt", {})

    return AppConfig(
        sensors=[SensorInfo(**sensor) for sensor in sensors_data],
        mqtt=MqttConfig(**mqtt_data),
    )