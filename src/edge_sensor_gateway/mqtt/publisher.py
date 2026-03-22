import json
from typing import Any

import paho.mqtt.client as mqtt


class MqttPublisher:
    def __init__(self, host: str = "localhost", port: int = 1883, enabled: bool = False) -> None:
        self.host = host
        self.port = port
        self.enabled = enabled
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.connected = False

    def connect(self) -> None:
        if not self.enabled:
            return

        try:
            self.client.connect(self.host, self.port, 60)
            self.client.loop_start()
            self.connected = True
            print(f"[MQTT] Connected to broker at {self.host}:{self.port}")
        except Exception as exc:
            print(f"[MQTT] Connection failed: {exc}")
            self.connected = False

    def publish(self, topic: str, payload: dict[str, Any]) -> None:
        if not self.enabled or not self.connected:
            return

        self.client.publish(topic, json.dumps(payload))

    def disconnect(self) -> None:
        if not self.enabled or not self.connected:
            return

        self.client.loop_stop()
        self.client.disconnect()
        self.connected = False
        print("[MQTT] Disconnected from broker")