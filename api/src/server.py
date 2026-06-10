from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from api.src.classes import Lamp, LampState
from api.src.utils import read_config

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("INICIALIZANDO APARELHOS (Garantido apenas 1 vez)")
    
    app.state.lamps = {lamp_data["device_id"]: Lamp(lamp_data) for lamp_data in read_config()}
    
    yield
    
    print("Shutting down server")


app = FastAPI(title="Smart Home API", lifespan=lifespan)


@app.patch("/lamps/{lamp_id}/state")
def update_lamp_status(lamp_id: str, state: LampState):
    lamp_dict = app.state.lamps
    if lamp_id not in lamp_dict:
        raise HTTPException(status_code=404, detail="Lamp not found. Make sure device id is valid.")
    lamp_dict[lamp_id].state = state
    return {
        "message": "Update successful",
        "online": lamp_dict[lamp_id].online,
        "new_state": lamp_dict[lamp_id].state
    }