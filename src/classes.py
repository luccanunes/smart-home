import tinytuya
from enum import Enum
from time import sleep

class RoutineBehaviour(str, Enum):
    IGNORE = "IGNORE"
    NORMAL = "NORMAL"
    DELAYED = "DELAYED"
    INSTANT = "INSTANT"

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
    
    def turn_off(self):
        self.tuya_device_object.turn_off()

    def turn_on(self):
        self.tuya_device_object.turn_on()

    def status(self):
        return self.tuya_device_object.status()
    
    def set_brightness(self, x):
        self.tuya_device_object.set_brightness_percentage(x)

    def set_colour_temperature(self, x):
        self.tuya_device_object.set_colourtemp_percentage(x)

    def set_white(self, brightness, colour_temperature):
        self.tuya_device_object.set_white_percentage(brightness, colour_temperature)

    def set_white(self, x):
        self.tuya_device_object.set_white_percentage(x, x)

    def execute_sunrise_routine(self, total_duration_minutes = 30, final_intensity = 100, num_steps = 10):
        if self.sunrise_behaviour == RoutineBehaviour.IGNORE: return

        total_duration_seconds = total_duration_minutes * 60
        step = final_intensity // num_steps
        num_timeouts = num_steps - 1
        timeout_seconds = total_duration_seconds / num_timeouts
        
        print(f"[INFO] Starting sunrise routine for lamp '{self.name}' | Mode: {self.sunrise_behaviour.value} | Duration: {total_duration_minutes} min")
        
        for i in range(1, final_intensity + step, step):
            print(f"set {i}, sleep {timeout_seconds}")
            self.set_white(i)
            sleep(timeout_seconds)

        

        
        