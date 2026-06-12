## Orchestrator

A Go client application for controlling lamps through the Smart Home API.

Status: Work in progress. The application structure is in place but the main functionality is not fully implemented. Currently the main function contains a hardcoded example that turns off a lamp.

### Building

```bash
go build -o orchestrator main.go
```

### Running

```bash
./orchestrator
```

### Usage

The `Lamp` struct represents a lamp and can send state changes to the API:

```go
lamp := Lamp{
    Name:     "Bedroom",
    DeviceID: "device_id_here",
}

state := LampState{
    TurnedOn: &[]bool{true}[0],
    Brightness: &[]int{75}[0],
}

err := lamp.SetState(state)
```

The `SetState` method makes a PATCH request to the API at `http://0.0.0.0:8000/lamps/{device_id}/state`.

### Configuration

Modify the `baseURL` constant in main.go to point to your API server if it is running on a different address or port.

### Notes

- The API must be running and reachable at the configured base URL for state changes to work
- Fields in `LampState` are pointers so they can be omitted in the JSON request (only set the fields you want to change)
