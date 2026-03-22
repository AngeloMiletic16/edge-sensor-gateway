FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
COPY configs ./configs
COPY docs ./docs
COPY tests ./tests

RUN pip install --upgrade pip && pip install -e ".[dev]"

EXPOSE 8000

CMD ["uvicorn", "edge_sensor_gateway.main:app", "--host", "0.0.0.0", "--port", "8000"]