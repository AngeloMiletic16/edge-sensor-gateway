# Test Plan

## Goal

The goal of testing is to verify the correctness, reliability, and maintainability of the Edge Sensor Gateway Simulator.

## Test scope

The following parts of the system are covered:

- alarm rule evaluation
- configuration loading
- API endpoint availability
- response structure of main endpoints

## Current tests

### Alarm engine tests
Verify that:
- a high temperature reading creates an alarm
- a normal temperature reading does not create an alarm

### Configuration tests
Verify that:
- YAML configuration is loaded successfully
- sensor definitions are parsed
- MQTT settings are available

### API tests
Verify that:
- `/health` returns HTTP 200
- `/sensors` returns HTTP 200
- response payloads have the expected format

## Future test extensions

The following tests should be added in future versions:
- WebSocket integration tests
- MQTT publisher tests with mocked broker
- gateway service async loop tests
- sensor factory tests
- negative configuration tests
- alarm tests for vibration and other sensor types

## Test tools

- pytest
- pytest-asyncio
- FastAPI TestClient

## Success criteria

The test phase is considered successful when:
- all automated tests pass
- the application starts successfully
- REST endpoints return valid responses
- live WebSocket event streaming works in manual testing