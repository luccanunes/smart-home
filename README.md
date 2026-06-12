# Smart Home

A system for controlling Tuya smart bulbs over a local network through an HTTP API and client applications.

## Projects

### API

A FastAPI server that exposes endpoints for controlling smart lamps. The server communicates with Tuya devices over the local network to update their state (power, brightness, color temperature).

See [api/README.md](api/README.md) for setup and usage.

### Orchestrator

A Go application that acts as a client to the API. It allows triggering lamp state changes through code.

Status: Work in progress. The application structure is in place but the main functionality is not fully implemented.

## Configuration

Lamps are configured in `config.json` at the repository root. Each lamp entry requires:

- `name`: Human-readable identifier
- `device_id`: Tuya device ID
- `ip`: Local IP address of the device
- `local_key`: Authentication key for the device
- `version`: Tuya protocol version (typically 3.5)
- `operation_mode`: Control mode (currently unused, reserved for future automation)

The configuration file should not be committed to version control as it contains device credentials.
