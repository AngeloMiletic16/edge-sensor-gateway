from edge_sensor_gateway.core.models import SensorInfo
from edge_sensor_gateway.sensors.base import BaseSensor
from edge_sensor_gateway.sensors.distance import DistanceSensor
from edge_sensor_gateway.sensors.temperature import TemperatureSensor
from edge_sensor_gateway.sensors.vibration import VibrationSensor


def create_sensor(sensor_info: SensorInfo) -> BaseSensor:
    if sensor_info.sensor_type == "temperature":
        return TemperatureSensor(sensor_info)

    if sensor_info.sensor_type == "distance":
        return DistanceSensor(sensor_info)

    if sensor_info.sensor_type == "vibration":
        return VibrationSensor(sensor_info)

    raise ValueError(f"Unsupported sensor type: {sensor_info.sensor_type}")