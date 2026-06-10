package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
)

type OperationMode int

const (
	Manual OperationMode = iota
	Circadian
	Party
)

const baseURL = "http://0.0.0.0:8000/lamps/"

type LampState struct {
	TurnedOn          *bool `json:"turned_on,omitempty"`
    Brightness        *int  `json:"brightness,omitempty"`
    ColourTemperature *int  `json:"colour_temperature,omitempty"`
}

type Lamp struct {
	Name string
	DeviceID string
	State LampState
	OperationMode OperationMode
}

func (lamp *Lamp) SetState(state LampState) error {
	requestURL := fmt.Sprintf("%s%s/state", baseURL, lamp.DeviceID)

	jsonData, err := json.Marshal(state)

	if err != nil {
		return err
	}

	req, err := http.NewRequest(http.MethodPatch, requestURL, bytes.NewBuffer(jsonData))

	if err != nil {
		return err
	}

	req.Header.Set("Content-Type", "application/json")
	client := &http.Client{}
	resp, err := client.Do(req)

	if err != nil {
		return err
	}

	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)

	if err != nil {
		return err
	}

	fmt.Println("[INFO] Status Code:", resp.StatusCode)
	fmt.Println("[INFO] Server response:\n", string(body))

	return nil
}

func main() {

	turnOn := false
	//brightness := 70
	// temp := 30

	onState := LampState{
		TurnedOn: &turnOn,
		//Brightness: &brightness,
		// ColourTemperature: &temp,
	}
	
	tableLamp := Lamp{
		Name: "Mesa",
	}

	err := tableLamp.SetState(onState)

	if err != nil {
		fmt.Println("[ERROR] Failed to set lamp state:", err)
	}

	
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
*/