def reading_topic(sensor_id: str) -> str:
    return f"factory/sensors/{sensor_id}/reading"


def status_topic(sensor_id: str) -> str:
    return f"factory/sensors/{sensor_id}/status"


def alarm_topic(severity: str) -> str:
    return f"factory/alarms/{severity}"


def gateway_health_topic() -> str:
    return "factory/gateway/health"