## Smart Home API

A REST API for controlling Tuya smart bulbs on a local network.

### Installation

Install dependencies:

```bash
pip install fastapi uvicorn tinytuya pydantic
```

### Configuration

Before running the server, create a `config.json` file in the repository root with your lamp definitions. Each lamp must have:

- `name`: Lamp identifier
- `device_id`: Tuya device ID
- `ip`: Device IP address on your local network
- `local_key`: Device authentication key
- `version`: Tuya protocol version (e.g., 3.5)

#### Getting Tuya Device Information

You need the device ID, local IP address, and local key to control each lamp.

1. **Install tinytuya**:

   ```bash
   pip install tinytuya
   ```

2. **Run the wizard to get the local key**:

   ```bash
   python -m tinytuya wizard
   ```

   This interactive wizard will help you extract the local key from your Tuya account. Follow the prompts to log in with your Tuya app credentials.

3. **Scan your network for device IPs**:

   ```bash
   python -m tinytuya scan
   ```

   This will discover all Tuya devices on your local network and display their device IDs and IP addresses.

4. **Find the protocol version**:

   Most Tuya devices use version 3.1 or 3.5. You can try both if unsure, or check your device documentation.

#### Example Configuration

```json
{
  "lamps": [
    {
      "name": "Bedroom",
      "device_id": "device_id_here",
      "ip": "192.168.1.100",
      "local_key": "your_local_key_here",
      "version": 3.5,
      "operation_mode": "CIRCADIAN"
    }
  ]
}
```

### Running the Server

From the repository root:

```bash
uvicorn api.src.server:app --host <IP_REDACTED> --port 8000
```

The server will start on `http://localhost:8000`. On startup, it initializes connections to all configured lamps and logs their status.

### API Endpoints

#### Update Lamp State

```
PATCH /lamps/{lamp_id}/state
```

Updates the state of a lamp. Only the fields you want to change need to be sent.

Request body:

```json
{
  "turned_on": true,
  "brightness": 75,
  "colour_temperature": 50
}
```

All fields are optional:

- `turned_on` (boolean): Turn the lamp on or off
- `brightness` (0-100): Brightness percentage
- `colour_temperature` (0-100): Color temperature percentage (warm to cold)

Response on success:

```json
{
  "message": "Update successful",
  "device_id": "device_id_here",
  "name": "Bedroom",
  "online": true,
  "new_state": {
    "turned_on": true,
    "brightness": 75,
    "colour_temperature": 50
  }
}
```

Error responses:

- `404 Not Found`: Lamp ID does not exist
- `503 Service Unavailable`: Lamp is offline or unreachable

### Notes

The API automatically handles device communication failures. If a lamp is offline during server startup, it will be marked as offline but the server will continue running. State updates to offline devices will return a 503 error.

Brightness values are internally converted to 0-100 percentage range (the API normalizes Tuya's 10-1000 range).
