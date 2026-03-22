from edge_sensor_gateway.config import load_app_config


def test_load_app_config_returns_sensors_and_mqtt():
    config = load_app_config()

    assert len(config.sensors) >= 1
    assert config.mqtt.host == "mosquitto"
    assert config.mqtt.port == 1883