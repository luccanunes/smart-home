package main

type LampState struct {
	turned_on bool
    brightness int
    colour_temperature int
}

type Lamp struct {
	name string
	// sunrise_behaviour RoutineBehaviour
	// sunset_behaviour RoutineBehaviour
	device_id string
	state LampState
}

/*
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
*/

func (lamp Lamp) turn_off() {
	
}

func main() {

}