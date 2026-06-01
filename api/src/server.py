from fastapi import FastAPI
from classes import Lamp, LampState

app = FastAPI(title="Smart Home API")

@app.patch("/lamps/{lamp_id}/state")
def update_lamp_status(lamp_id: str, state: LampState):
    return {"status": "Servidor online", "sistema": "Tuya Local"}