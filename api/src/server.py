from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from api.src.classes import Lamp, LampState, DeviceOfflineError
from api.src.utils import read_config

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up server")
    
    app.state.lamps = {lamp_data["device_id"]: Lamp(lamp_data) for lamp_data in read_config()}
    
    yield
    
    print("Shutting down server")


app = FastAPI(title="Smart Home API", lifespan=lifespan)


@app.patch("/lamps/{lamp_id}/state")
def update_lamp_status(lamp_id: str, state: LampState):
    lamp_dict = app.state.lamps

    if lamp_id not in lamp_dict:
        raise HTTPException(status_code=404, detail="Device not found. Make sure device id is valid.")
    
    try:
        lamp_dict[lamp_id].state = state
    except DeviceOfflineError as e:
        raise HTTPException(status_code=503, detail=f"Failed to update device state. It is likely offline: {e}",)

    return {
        "message": "Update successful",
        "device_id": lamp_dict[lamp_id].device_id,
        "name": lamp_dict[lamp_id].name,
        "online": lamp_dict[lamp_id].online,
        "new_state": lamp_dict[lamp_id].state
    }