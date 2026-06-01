from fastapi import FastAPI, HTTPException
from classes import Lamp, LampState
from utils import read_config

app = FastAPI(title="Smart Home API")

lamp_dict = {lamp_data["device_id"]: Lamp(lamp_data) for lamp_data in read_config()}

@app.patch("/lamps/{lamp_id}/state")
def update_lamp_status(lamp_id: str, state: LampState):
    if lamp_id not in lamp_dict:
        raise HTTPException(status_code=404, detail="Lamp not found. Make sure device id is valid.")
    lamp_dict[lamp_id].state = state
    return {
        "message": "Update successful",
        "new_state": lamp_dict[lamp_id].state
    }