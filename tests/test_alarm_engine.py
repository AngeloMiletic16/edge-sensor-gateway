from edge_sensor_gateway.alarms.engine import AlarmEngine
from edge_sensor_gateway.core.models import SensorReading


def test_temperature_alarm_is_created_for_high_value():
    engine = AlarmEngine()

    reading = SensorReading(
        sensor_id="temp-001",
        sensor_type="temperature",
        value=29.5,
        unit="C",
    )

    alarm = engine.evaluate(reading)

    assert alarm is not None
    assert alarm.sensor_id == "temp-001"
    assert alarm.severity == "warning"


def test_no_alarm_for_normal_temperature():
    engine = AlarmEngine()

    reading = SensorReading(
        sensor_id="temp-001",
        sensor_type="temperature",
        value=24.0,
        unit="C",
    )

    alarm = engine.evaluate(reading)

    assert alarm is None