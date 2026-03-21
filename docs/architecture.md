# Architecture

## Purpose

The Edge Sensor Gateway Simulator models a small industrial edge application that collects sensor telemetry, evaluates alarm conditions, and distributes data to external consumers.

## Main components

### Sensors
Sensor classes simulate hardware devices and generate readings asynchronously.

Implemented sensor types:
- temperature
- distance
- vibration

### Gateway service
The gateway service is the orchestration layer of the system. It:
- loads configuration
- creates sensor instances
- runs sensor tasks concurrently
- stores latest readings
- evaluates alarms
- broadcasts events
- publishes MQTT messages

### Storage
An in-memory storage layer keeps:
- configured sensors
- latest readings
- collected alarms
- health counters

### Alarm engine
The alarm engine evaluates incoming sensor readings and creates alarm events when thresholds are exceeded.

### API layer
FastAPI provides:
- REST endpoints for current state
- WebSocket endpoint for real-time events
- simple HTML viewer for manual WebSocket testing

### MQTT layer
The MQTT publisher sends:
- sensor readings
- alarm events
- gateway health information

## Data flow

1. Sensor configuration is loaded from YAML.
2. Sensor objects are created through a factory.
3. Each sensor runs in its own async loop.
4. New readings are stored in memory.
5. Readings are broadcast through WebSocket.
6. Readings are optionally published to MQTT.
7. Alarm engine evaluates the reading.
8. Generated alarms are stored, broadcast, and optionally published to MQTT.

## Design goals

- modular structure
- asynchronous execution
- clean separation of responsibilities
- easy extensibility through configuration and sensor factory pattern
- support for testing and CI