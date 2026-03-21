from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from edge_sensor_gateway.gateway.service import GatewayService

gateway_service = GatewayService()
app = FastAPI(title="Edge Sensor Gateway Simulator")


@app.on_event("startup")
async def startup_event() -> None:
    import asyncio
    asyncio.create_task(gateway_service.run())


@app.get("/")
async def root():
    return {
        "message": "Edge Sensor Gateway Simulator is running",
        "docs": "/docs",
        "websocket": "/ws/readings",
        "viewer": "/viewer",
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