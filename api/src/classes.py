import tinytuya
from enum import Enum
from time import sleep
from pydantic import BaseModel
from typing import Optional

class RoutineBehaviour(str, Enum):
    IGNORE = "IGNORE"
    NORMAL = "NORMAL"
    DELAYED = "DELAYED"

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
        
        self.name = lamp_dict["name"]
        self.sunrise_behaviour = RoutineBehaviour(lamp_dict.get("sunrise_behaviour", "IGNORE"))
        self.sunset_behaviour = RoutineBehaviour(lamp_dict.get("sunset_behaviour", "IGNORE"))

        self.tuya_device_object = tinytuya.BulbDevice(
            lamp_dict["device_id"],
            lamp_dict["ip"],
            lamp_dict["local_key"]
        )
        self.tuya_device_object.set_version(lamp_dict["version"])
        self._state = LampState()

    @property
    def state(self) -> LampState:
        return self._state

    @state.setter
    def state(self, new_state: LampState):
        if new_state.turned_on is not None:
            if new_state.turned_on and not self._state.turned_on:
                self.turn_on()
            elif not new_state.turned_on and self._state.turned_on:
                self.turn_off()

        if new_state.brightness is not None and new_state.colour_temperature is not None:
            self.set_white(new_state.brightness, new_state.colour_temperature)
        elif new_state.brightness is not None and new_state.brightness != self._state.brightness:
            self.set_brightness(new_state.brightness)
        elif new_state.colour_temperature is not None and new_state.colour_temperature != self._state.colour_temperature:
            self.set_colour_temperature(new_state.colour_temperature)
    
    def turn_off(self):
        self.tuya_device_object.turn_off()
        self._state.turned_on = False

    def turn_on(self):
        self.tuya_device_object.turn_on()
        self._state.turned_on = True

    def status(self):
        return self.tuya_device_object.status()
    
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

    # def execute_sunrise_routine(self, total_duration_minutes = 30, final_intensity = 100, num_steps = 10):
    #     if self.sunrise_behaviour == RoutineBehaviour.IGNORE: return

    #     initial_intensity = 1
    #     if self.sunrise_behaviour == RoutineBehaviour.DELAYED:
    #         initial_intensity = final_intensity // 2

    #     total_duration_seconds = total_duration_minutes * 60        
    #     timeout_seconds = total_duration_seconds / num_steps
    #     intensity_range = final_intensity - initial_intensity
        
    #     print(f"[INFO] Starting sunrise routine for lamp '{self.name}' | Mode: {self.sunrise_behaviour.value} | Duration: {total_duration_minutes} min")

    #     print(f"[{self.name}] set {initial_intensity}, sleep {timeout_seconds}")
    #     self.set_white(initial_intensity)
    #     sleep(timeout_seconds)

    #     for step_current in range(1, num_steps + 1):
    #         progress = step_current / num_steps
    #         calculated_intensity = int(initial_intensity + (intensity_range * progress))
            
    #         print(f"[{self.name}] set {calculated_intensity}, sleep {timeout_seconds} {step_current < num_steps}")
    #         self.set_white(calculated_intensity)

    #         if step_current < num_steps:
    #             sleep(timeout_seconds)