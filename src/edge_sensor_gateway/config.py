from pathlib import Path

import yaml

from edge_sensor_gateway.core.models import SensorInfo


def load_sensor_config(config_path: str = "configs/sensors.example.yaml") -> list[SensorInfo]:
    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    sensors_data = data.get("sensors", [])
    return [SensorInfo(**sensor) for sensor in sensors_data]