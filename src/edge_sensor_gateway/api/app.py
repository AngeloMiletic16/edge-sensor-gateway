import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from edge_sensor_gateway.gateway.service import GatewayService

gateway_service = GatewayService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(gateway_service.run())
    try:
        yield
    finally:
        task.cancel()
        gateway_service.mqtt_publisher.disconnect()


app = FastAPI(title="Edge Sensor Gateway Simulator", lifespan=lifespan)


@app.get("/")
async def root():
    return {
        "message": "Edge Sensor Gateway Simulator is running",
        "docs": "/docs",
        "websocket": "/ws/readings",
        "viewer": "/viewer",
        "dashboard": "/dashboard",
    }


@app.get("/viewer")
async def viewer():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>WebSocket Viewer</title>
    </head>
    <body>
        <h1>Edge Sensor Gateway WebSocket Viewer</h1>
        <button onclick="connect()">Connect</button>
        <ul id="messages"></ul>

        <script>
            let socket;
            let pingInterval;

            function connect() {
                socket = new WebSocket("ws://127.0.0.1:8000/ws/readings");

                socket.onopen = function () {
                    const item = document.createElement("li");
                    item.textContent = "Connected to WebSocket";
                    document.getElementById("messages").appendChild(item);

                    pingInterval = setInterval(() => {
                        if (socket.readyState === WebSocket.OPEN) {
                            socket.send("ping");
                        }
                    }, 1000);
                };

                socket.onmessage = function (event) {
                    const item = document.createElement("li");
                    item.textContent = event.data;
                    document.getElementById("messages").appendChild(item);
                };

                socket.onclose = function () {
                    const item = document.createElement("li");
                    item.textContent = "Disconnected";
                    document.getElementById("messages").appendChild(item);

                    if (pingInterval) {
                        clearInterval(pingInterval);
                    }
                };
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)


@app.get("/dashboard")
async def dashboard():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Edge Sensor Gateway Dashboard</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 24px;
                background: #f5f7fb;
                color: #1f2937;
            }

            h1, h2 {
                margin-bottom: 12px;
            }

            .grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 16px;
                margin-bottom: 24px;
            }

            .card {
                background: white;
                border-radius: 12px;
                padding: 16px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            }

            .badge {
                display: inline-block;
                padding: 4px 10px;
                border-radius: 999px;
                font-size: 12px;
                font-weight: bold;
                background: #dbeafe;
                color: #1d4ed8;
            }

            .alarm-badge {
                background: #fee2e2;
                color: #b91c1c;
            }

            ul {
                padding-left: 18px;
            }

            li {
                margin-bottom: 8px;
            }

            .event-feed {
                max-height: 320px;
                overflow-y: auto;
                background: #111827;
                color: #f9fafb;
                padding: 12px;
                border-radius: 12px;
                font-family: Consolas, monospace;
                font-size: 13px;
            }

            .event-feed div {
                margin-bottom: 10px;
                border-bottom: 1px solid #374151;
                padding-bottom: 8px;
            }

            .muted {
                color: #6b7280;
                font-size: 14px;
            }

            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 8px;
            }

            th, td {
                text-align: left;
                padding: 8px;
                border-bottom: 1px solid #e5e7eb;
                font-size: 14px;
            }

            th {
                background: #f9fafb;
            }
        </style>
    </head>
    <body>
        <h1>Edge Sensor Gateway Dashboard</h1>
        <p class="muted">Live monitoring dashboard for simulated industrial sensors.</p>

        <div class="grid">
            <div class="card">
                <h2>Health</h2>
                <p>Status: <span class="badge" id="health-status">loading...</span></p>
                <p>Active sensors: <strong id="health-sensors">-</strong></p>
                <p>Total readings: <strong id="health-readings">-</strong></p>
                <p>Active alarms: <strong id="health-alarms">-</strong></p>
            </div>

            <div class="card">
                <h2>Configured Sensors</h2>
                <ul id="sensor-list"></ul>
            </div>

            <div class="card">
                <h2>Active Alarms</h2>
                <ul id="alarm-list"></ul>
            </div>
        </div>

        <div class="grid">
            <div class="card">
                <h2>Latest Readings</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Sensor ID</th>
                            <th>Type</th>
                            <th>Value</th>
                            <th>Unit</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody id="readings-table"></tbody>
                </table>
            </div>

            <div class="card">
                <h2>Live Event Feed</h2>
                <div class="event-feed" id="event-feed"></div>
            </div>
        </div>

        <script>
            const sensorList = document.getElementById("sensor-list");
            const alarmList = document.getElementById("alarm-list");
            const readingsTable = document.getElementById("readings-table");
            const eventFeed = document.getElementById("event-feed");

            async function loadInitialData() {
                const [healthRes, sensorsRes, readingsRes, alarmsRes] = await Promise.all([
                    fetch("/health"),
                    fetch("/sensors"),
                    fetch("/readings/latest"),
                    fetch("/alarms")
                ]);

                const health = await healthRes.json();
                const sensors = await sensorsRes.json();
                const readings = await readingsRes.json();
                const alarms = await alarmsRes.json();

                renderHealth(health);
                renderSensors(sensors);
                renderReadings(readings);
                renderAlarms(alarms);
            }

            function renderHealth(health) {
                document.getElementById("health-status").textContent = health.status;
                document.getElementById("health-sensors").textContent = health.active_sensors;
                document.getElementById("health-readings").textContent = health.total_readings;
                document.getElementById("health-alarms").textContent = health.active_alarms;
            }

            function renderSensors(sensors) {
                sensorList.innerHTML = "";
                sensors.forEach(sensor => {
                    const li = document.createElement("li");
                    li.textContent = `${sensor.sensor_id} — ${sensor.sensor_type} (${sensor.interval_seconds}s)`;
                    sensorList.appendChild(li);
                });
            }

            function renderReadings(readings) {
                readingsTable.innerHTML = "";
                readings.forEach(reading => {
                    const row = document.createElement("tr");
                    row.innerHTML = `
                        <td>${reading.sensor_id}</td>
                        <td>${reading.sensor_type}</td>
                        <td>${reading.value}</td>
                        <td>${reading.unit}</td>
                        <td>${reading.status}</td>
                    `;
                    readingsTable.appendChild(row);
                });
            }

            function renderAlarms(alarms) {
                alarmList.innerHTML = "";

                if (!alarms.length) {
                    const li = document.createElement("li");
                    li.textContent = "No alarms yet";
                    alarmList.appendChild(li);
                    return;
                }

                alarms.slice(-10).reverse().forEach(alarm => {
                    const li = document.createElement("li");
                    li.innerHTML = `<span class="badge alarm-badge">${alarm.severity}</span> ${alarm.sensor_id} — ${alarm.message}`;
                    alarmList.appendChild(li);
                });
            }

            function addEventLine(eventData) {
                const entry = document.createElement("div");
                entry.textContent = JSON.stringify(eventData);
                eventFeed.prepend(entry);

                while (eventFeed.children.length > 30) {
                    eventFeed.removeChild(eventFeed.lastChild);
                }
            }

            async function refreshHealthAndAlarms() {
                const [healthRes, alarmsRes, readingsRes] = await Promise.all([
                    fetch("/health"),
                    fetch("/alarms"),
                    fetch("/readings/latest")
                ]);

                const health = await healthRes.json();
                const alarms = await alarmsRes.json();
                const readings = await readingsRes.json();

                renderHealth(health);
                renderAlarms(alarms);
                renderReadings(readings);
            }

            function connectWebSocket() {
                const socket = new WebSocket("ws://127.0.0.1:8000/ws/readings");

                socket.onopen = function () {
                    addEventLine({ event_type: "system", payload: "WebSocket connected" });

                    setInterval(() => {
                        if (socket.readyState === WebSocket.OPEN) {
                            socket.send("ping");
                        }
                    }, 1000);
                };

                socket.onmessage = function (event) {
                    const parsed = JSON.parse(event.data);
                    addEventLine(parsed);
                    refreshHealthAndAlarms();
                };

                socket.onclose = function () {
                    addEventLine({ event_type: "system", payload: "WebSocket disconnected" });
                };
            }

            loadInitialData();
            connectWebSocket();
            setInterval(refreshHealthAndAlarms, 5000);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)


@app.get("/health")
async def get_health():
    return gateway_service.storage.get_health()


@app.get("/sensors")
async def get_sensors():
    return gateway_service.storage.get_sensors()


@app.get("/readings/latest")
async def get_latest_readings():
    return gateway_service.storage.get_latest_readings()


@app.get("/alarms")
async def get_alarms():
    return gateway_service.storage.get_alarms()


@app.websocket("/ws/readings")
async def websocket_readings(websocket: WebSocket):
    manager = gateway_service.broadcaster.manager
    await manager.connect(websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)