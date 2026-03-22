Edge Sensor Gateway Simulator
=============================

A Python-based industrial edge gateway simulator for asynchronous sensor data collection, alarm detection, and communication over REST, WebSocket, and MQTT.

📋 Overview
-----------

This project simulates a small industrial edge gateway that collects telemetry from multiple sensors, processes readings asynchronously, evaluates alarm conditions, and exposes data to external systems.

It was designed as a portfolio project for Python roles related to:

*   embedded and edge-style systems
*   industrial automation software
*   asynchronous programming with `asyncio`
*   communication protocols such as HTTP, WebSocket, and MQTT
*   modular Python package design
*   automated testing and CI/CD workflows

🚀 Features
-----------

*   **Multi-Sensor Simulation**  
    Simulates temperature, distance, and vibration sensors with configurable polling intervals.
*   **Async Data Collection**  
    Uses Python `asyncio` to run multiple sensor loops concurrently.
*   **Alarm Detection**  
    Generates alarms when sensor readings exceed defined thresholds.
*   **REST API**  
    Exposes current system state through FastAPI endpoints.
*   **WebSocket Live Stream**  
    Broadcasts sensor readings and alarm events in real time.
*   **MQTT Publishing**  
    Publishes sensor telemetry, alarm events, and gateway health information to MQTT topics.
*   **YAML Configuration**  
    Loads sensor and MQTT settings from a configuration file.
*   **Automated Testing**  
    Includes initial unit and API tests with `pytest`.
*   **CI Pipeline**  
    Supports linting, type checking, and automated tests through GitHub Actions.

🛠️ Tech Stack
--------------

*   **Python 3.11+**
*   **FastAPI**
*   **asyncio**
*   **Pydantic**
*   **PyYAML**
*   **paho-mqtt**
*   **pytest**
*   **Ruff**
*   **MyPy**
*   **GitHub Actions**

📂 Project Structure
--------------------

edge-sensor-gateway/  
├── .github/  
│   └── workflows/  
│       └── ci.yml  
├── configs/  
│   └── sensors.example.yaml  
├── docs/  
│   ├── architecture.md  
│   └── test\_plan.md  
├── src/  
│   └── edge\_sensor\_gateway/  
│       ├── alarms/  
│       ├── api/  
│       ├── core/  
│       ├── gateway/  
│       ├── mqtt/  
│       ├── sensors/  
│       ├── storage/  
│       ├── utils/  
│       ├── config.py  
│       └── main.py  
├── tests/  
│   ├── test\_alarm\_engine.py  
│   ├── test\_api.py  
│   └── test\_config.py  
├── .gitignore  
├── pyproject.toml  
└── README.md

⚙️ Configuration
----------------

The application loads configuration from:

`configs/sensors.example.yaml`

### Example configuration

mqtt:  
  enabled: false  
  host: localhost  
  port: 1883  
  
sensors:  
  - sensor\_id: temp-001  
    name: Temperature Sensor 1  
    sensor\_type: temperature  
    unit: C  
    interval\_seconds: 2.0  
  
  - sensor\_id: dist-001  
    name: Distance Sensor 1  
    sensor\_type: distance  
    unit: mm  
    interval\_seconds: 3.0  
  
  - sensor\_id: vib-001  
    name: Vibration Sensor 1  
    sensor\_type: vibration  
    unit: g  
    interval\_seconds: 4.0

📡 API Endpoints
----------------

The project currently exposes the following endpoints:

*   `GET /` — basic service information
*   `GET /health` — gateway health status
*   `GET /sensors` — configured sensors
*   `GET /readings/latest` — latest readings from all sensors
*   `GET /alarms` — collected alarm events
*   `GET /viewer` — simple browser-based WebSocket event viewer
*   `WS /ws/readings` — live event stream for readings and alarms

🧠 Architecture
---------------

The system is organized into several logical layers:

### 1\. Sensors

Sensor classes simulate industrial devices and generate readings asynchronously.

Implemented sensor types:

*   `temperature`
*   `distance`
*   `vibration`

### 2\. Gateway Service

The gateway service is the orchestration layer. It:

*   loads configuration
*   creates sensor instances
*   starts concurrent async sensor tasks
*   stores new readings
*   evaluates alarm conditions
*   broadcasts events to WebSocket clients
*   publishes data to MQTT when enabled

### 3\. Storage

An in-memory storage layer keeps:

*   configured sensors
*   latest sensor readings
*   collected alarms
*   health counters

### 4\. Alarm Engine

The alarm engine evaluates sensor readings and creates alarm events when rules are triggered.

### 5\. API Layer

FastAPI provides:

*   REST endpoints for current state
*   WebSocket endpoint for live event streaming
*   simple HTML page for manual WebSocket testing

### 6\. MQTT Layer

The MQTT publisher is responsible for publishing:

*   sensor readings
*   alarm events
*   gateway health data

🔄 Data Flow
------------

1.  Sensor and MQTT configuration is loaded from YAML.
2.  Sensor instances are created through a factory.
3.  Each sensor runs in its own async loop.
4.  New readings are stored in memory.
5.  Readings are broadcast through WebSocket.
6.  Readings are optionally published to MQTT.
7.  Alarm rules are evaluated.
8.  Generated alarms are stored, broadcast, and optionally published to MQTT.

🛠️ Installation
----------------

### Prerequisites

*   Python 3.11 or higher
*   `pip`
*   optional: an MQTT broker such as Mosquitto if MQTT publishing is enabled

### Setup

Clone the repository:

git clone https://github.com/AngeloMiletic16/edge-sensor-gateway.git  
cd edge-sensor-gateway

Create and activate a virtual environment:

python \-m venv .venv

On Windows PowerShell:

.venv\\Scripts\\Activate.ps1

Install the project:

pip install \-e .

Install development tools:

pip install \-e ".\[dev\]"

▶️ Usage
--------

Run the application locally:

uvicorn edge\_sensor\_gateway.main:app \--reload

Open the API docs:

`http://127.0.0.1:8000/docs`

Open the WebSocket event viewer:

`http://127.0.0.1:8000/viewer`


## 🐳 Docker Usage

Run the full application stack with Docker Compose:

```bash 
docker compose up --build


📊 Example Output
-----------------

### Sensor reading event

{  
  "event\_type": "reading",  
  "payload": {  
    "sensor\_id": "temp-001",  
    "sensor\_type": "temperature",  
    "timestamp": "2026-03-21T10:15:30.123Z",  
    "value": 28.7,  
    "unit": "C",  
    "status": "ok"  
  }  
}

### Alarm event

{  
  "event\_type": "alarm",  
  "payload": {  
    "alarm\_id": "6f4df8e3-0c5d-4c12-98f0-64a9bb9d6a11",  
    "sensor\_id": "temp-001",  
    "sensor\_type": "temperature",  
    "severity": "warning",  
    "message": "High temperature detected: 28.7 C",  
    "timestamp": "2026-03-21T10:15:30.456Z",  
    "active": true  
  }  
}

🧪 Testing
----------

Run all tests:

pytest

Run linting:

ruff check .

Run type checking:

mypy src

✅ Current Status
----------------

Implemented:

*   multiple simulated sensors
*   asynchronous gateway service
*   alarm engine
*   REST API
*   WebSocket broadcasting
*   YAML configuration
*   MQTT publishing foundation
*   automated tests
*   GitHub Actions CI setup

🔧 CI / Quality Checks
----------------------

The GitHub Actions pipeline is configured to run:

*   Ruff linting
*   MyPy type checking
*   `pytest` test suite

This helps keep the project consistent and maintainable.

📚 Documentation
----------------

Additional project documentation:

*   `docs/architecture.md`
*   `docs/test_plan.md`

🎯 Why This Project
-------------------

This project was built to demonstrate practical skills relevant to Python positions involving:

*   industrial automation
*   sensor data processing
*   edge / embedded-adjacent development
*   async programming
*   testing and documentation
*   communication protocols used in real systems

🔮 Future Improvements
----------------------

*   Docker setup with integrated MQTT broker
*   richer alarm rules and severity levels
*   persistent storage
*   dashboard UI for live monitoring
*   broader integration test coverage
*   sensor plugin extensibility
*   health and metrics improvements