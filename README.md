# Edge Sensor Gateway Simulator

A modular Python-based industrial edge gateway simulator for asynchronous sensor data collection, validation, alarm handling, and communication over HTTP, WebSocket, and MQTT.

## Goal

This project simulates an industrial edge gateway that collects data from multiple sensors, processes readings asynchronously, detects alarms, and exposes data through REST API, WebSocket, and MQTT interfaces.

## Planned features

- simulated industrial sensors
- asynchronous data collection with asyncio
- alarm detection and health monitoring
- REST API with FastAPI
- WebSocket live stream
- MQTT publishing
- automated tests with pytest
- Docker support
- CI/CD with GitHub Actions

## Configuration

Sensor instances are loaded from a YAML configuration file located at:

`configs/sensors.example.yaml`

This allows the gateway to be configured without changing the application code.