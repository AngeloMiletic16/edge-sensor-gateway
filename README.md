# 🚀 Edge Sensor Gateway Simulator

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI Pipeline](https://github.com/AngeloMiletic16/edge-sensor-gateway/actions/workflows/ci.yml/badge.svg)](https://github.com/AngeloMiletic16/edge-sensor-gateway/actions)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)

A professional, high-performance industrial edge gateway simulator built with Python. This project simulates asynchronous sensor data collection, real-time alarm detection, and multi-protocol communication (REST, WebSocket, and MQTT).

---

## 📋 Overview

This project simulates a modular industrial edge gateway that collects telemetry from multiple simulated sensors (Temperature, Distance, Vibration), processes readings asynchronously, evaluates alarm conditions based on thresholds, and exposes the data to external systems.

**Key design goals:**
*   Demonstrate mastery of **Python Asyncio** for high-concurrency tasks.
*   Implement industrial communication standards (**MQTT, WebSockets**).
*   Showcase modern **Clean Architecture** and modular package design.
*   Ensure reliability through **Automated Testing** and **CI/CD** workflows.

---

## 📸 Screenshots

### Live Monitoring Dashboard
![Dashboard Screenshot](assets/dashboard.png)

### API Documentation (Swagger UI)
![API Docs Screenshot](assets/api-docs.png)

---

## 🚀 Features

*   **Multi-Sensor Simulation**: Simulates temperature, distance, and vibration sensors with configurable polling intervals and noise.
*   **Async Data Collection**: Uses `asyncio` to run multiple sensor loops concurrently without blocking.
*   **Real-time Alarm Engine**: Evaluates readings instantly and generates alarm events when thresholds are exceeded.
*   **Triple-Stream Communication**:
    *   **REST API**: FastAPI endpoints for system state, health, and history.
    *   **WebSocket Stream**: Live broadcast of sensor readings and alarms to connected clients.
    *   **MQTT Publishing**: Integration with industrial brokers for telemetry and gateway health.
*   **YAML Configuration**: Flexible sensor and MQTT settings management via configuration files.
*   **Quality Driven**: Built with strict type checking (MyPy), linting (Ruff), and unit testing (Pytest).

---

## 🛠️ Tech Stack

| Category | Technology |
| :--- | :--- |
| **Language** | Python 3.11+ |
| **Framework** | FastAPI (ASGI) |
| **Concurrency** | Asyncio |
| **Data Handling** | Pydantic, PyYAML |
| **Messaging** | Paho-MQTT, WebSockets |
| **Testing** | Pytest |
| **Tooling** | Ruff (Linter), MyPy (Types), Docker, GitHub Actions |

---

## 📂 Project Structure

```text
edge-sensor-gateway/
├── .github/workflows/      # GitHub Actions CI configurations
├── assets/                 # Screenshots and media
├── configs/                # YAML configuration templates
├── docker/                 # Infrastructure configs (e.g., Mosquitto)
├── docs/                   # Extended documentation (Architecture, Test Plans)
├── src/
│   └── edge_sensor_gateway/
│       ├── alarms/         # Alarm detection logic
│       ├── api/            # FastAPI routes & WebSocket handlers
│       ├── core/           # Interfaces and shared models
│       ├── gateway/        # Central orchestration service
│       ├── mqtt/           # MQTT publisher logic
│       ├── sensors/        # Async sensor simulators
│       ├── storage/        # Thread-safe in-memory state
│       └── main.py         # Application entry point
├── tests/                  # Pytest suite
├── Dockerfile              # Containerization
├── docker-compose.yml      # Full stack orchestration
└── pyproject.toml          # Build system and dependencies

## ⚙️ Configuration

The application loads its behavior from `configs/sensors.example.yaml`. You can define custom sensors and connection parameters here:

```yaml
mqtt:
  enabled: true
  host: localhost
  port: 1883

sensors:
  - sensor_id: temp-001
    name: Temperature Sensor 1
    sensor_type: temperature
    unit: C
    interval_seconds: 2.0

  - sensor_id: vib-001
    name: Vibration Sensor 1
    sensor_type: vibration
    unit: g
    interval_seconds: 4.0

### 🚀 API & Integration
**REST Endpoints**
- `GET /health` — Gateway status & uptime.
- `GET /sensors` — List active simulated sensors.
- `GET /readings/latest` — Latest data from all sensors.
- `GET /alarms` — History of triggered events.
- `GET /viewer` — Browser-based WebSocket visualizer.

**Real-time Streams**
- **WebSocket**: `WS /ws/readings` — Live JSON stream of readings/alarms.
- **MQTT Topics**: `gateway/telemetry` (Readings), `gateway/alarms` (Events), `gateway/health` (Heartbeat).

### 🔄 Data Flow
1. **Ingestion**: Async tasks generate telemetry via YAML config.
2. **Storage**: In-memory state management.
3. **Processing**: Alarm Engine validates safety bounds.
4. **Broadcasting**: Data pushed to WebSockets & MQTT.
5. **Consumption**: External apps consume data via REST/Streams.

### 🛠️ Setup & Usage
**Prerequisites:** Python 3.11+ | [Optional] MQTT Broker

**Local Setup:**
```bash
git clone https://github.com/AngeloMiletic16/edge-sensor-gateway.git
cd edge-sensor-gateway
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
uvicorn src.edge_sensor_gateway.main:app --reload

**Docker Setup**

docker compose up --build

###🧪 Testing & Quality
pytest        # Run tests
ruff check .  # Linting
mypy src      # Type analysis

###📊 Example Output

### Sensor Reading
{
    *event_type*: *reading*,
    *payload*: {
    *sensor_id*: *temp-**001***,
    *value*: 28.7,
    *unit*: *C*,
    *status*: *ok*
    }
}

###🎯 Project Goals

Demonstrating proficiency in:

Industrial IoT — Bridging edge sensors to cloud protocols. Concurrency — High-efficiency I/O using Python asyncio. **API** Design — Clean, documented **REST** and streaming interfaces. Reliability — Strong typing and modern CI/CD standards. 🔮 Roadmap InfluxDB/PostgreSQL persistence React-based dashboard Modbus/**TCP** and **OPC**-UA support ML-based anomaly detection

Developed by Angelo Miletic
