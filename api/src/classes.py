import tinytuya
from enum import Enum
from pydantic import BaseModel
from typing import Optional

class LampState(BaseModel):
    turned_on: Optional[bool] = None
    brightness: Optional[int] = None
    colour_temperature: Optional[int] = None

class Lamp:
    def __init__(self, lamp_dict):
        required_keys = ["name", "device_id", "ip", "local_key", "version"]
        for required_key in required_keys:
            if required_key not in lamp_dict:
                raise KeyError(f"Missing key in Lamp object: {required_key}")
        
        self.device_id = lamp_dict["device_id"]
        self.name = lamp_dict["name"]

        self.tuya_device_object = tinytuya.BulbDevice(
            lamp_dict["device_id"],
            lamp_dict["ip"],
            lamp_dict["local_key"]
        )
        self.tuya_device_object.set_version(lamp_dict["version"])

        try:
            current_status = self.tuya_device_object.state() or {}

            turned_on = current_status.get("is_on")
            brightness = current_status.get("brightness")
            colour_temperature = current_status.get("colourtemp")

            self._state = LampState(
                turned_on=bool(turned_on) if turned_on is not None else None,
                brightness=(brightness // 10) if brightness is not None else None,
                colour_temperature=(colour_temperature // 10) if colour_temperature is not None else None,
            )
            self.online = True
            print(f"[INFO] Lamp {self.name} online and correctly configured with state {self._state}")
        except RuntimeError:
            self._state = LampState(
                turned_on=None,
                brightness=None,
                colour_temperature=None
            )
            self.online = False
            print(f"[INFO] Lamp {self.name} could not be reached and has been configured with null state {self._state}")
        

    @property
    def state(self) -> LampState:
        return self._state

    @state.setter
    def state(self, new_state: LampState):
        '''
        TODO: currently, setting brightness to 50 on a turned off lamp will turn on the lamp but not update its turned on state
        we should define what is expected here:
        - should we really turn it on?
        - should we take note that the brightness should be changed but only do it when the lamp is on again?
        
        TODO: currently, if the lamp is offline on server startup, the state updates are inconsistent
        e.g., i can not seem to get the lamp to turn on by only sending the turned_on field
        - need to investigate how to handle with offline lamps
        '''
        print(f"[INFO] Setting new state of lamp '{self.name}' to {new_state}. Previous state: {self._state}")
        if new_state.turned_on is not None:
            if new_state.turned_on == True and self._state.turned_on != True:
                print(f"\t[INFO] Turning on lamp")
                self.turn_on()
            elif new_state.turned_on == False and self._state.turned_on != False:
                print(f"\t[INFO] Turning off lamp")
                self.turn_off()

        if new_state.brightness is not None and new_state.colour_temperature is not None:
            print(f"\t[INFO] Setting brightness to {new_state.brightness} and colour temperature to {new_state.colour_temperature}")
            self.set_white(new_state.brightness, new_state.colour_temperature)
        elif new_state.brightness is not None and new_state.brightness != self._state.brightness:
            print(f"\t[INFO] Setting brightness to {new_state.brightness}")
            self.set_brightness(new_state.brightness)
        elif new_state.colour_temperature is not None and new_state.colour_temperature != self._state.colour_temperature:
            print(f"\t[INFO] Setting colour temperature to {new_state.colour_temperature}")
            self.set_colour_temperature(new_state.colour_temperature)
    
    def turn_off(self):
        self.tuya_device_object.turn_off()
        self._state.turned_on = False

    def turn_on(self):
        self.tuya_device_object.turn_on()
        self._state.turned_on = True
    
    def set_brightness(self, x):
        self.tuya_device_object.set_brightness_percentage(x)
        self._state.brightness = x

    def set_colour_temperature(self, x):
        self.tuya_device_object.set_colourtemp_percentage(x)
        self._state.colour_temperature = x

    def set_white(self, brightness, colour_temperature=None):
        if colour_temperature is None:
            colour_temperature = brightness
        self.tuya_device_object.set_white_percentage(brightness, colour_temperature)
        self._state.brightness = brightness
        self._state.colour_temperature = colour_temperature