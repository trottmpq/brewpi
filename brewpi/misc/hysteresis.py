#!python

import requests
import time

def get_temp(temp_id):
    resp = requests.get(f'http://localhost:5000/devices/TempSensor/{temp_id}/temperature')
    return resp.get("temperature")

def set_heater(heater_id, onoff):
    requests.put(f'http://127.0.0.1:5000/devices/Heater/{heater_id}/state', json={'state': onoff})

def temp_loop(heater, temp, target_temp):
    """Hysterises loop to turn hold the kettle as a set temperature."""
    hyst_window = 1
    while True:
        temp_c = get_temp(temp)  # Current temperature

        if temp_c > target_temp + hyst_window:
            set_heater(heater, False)
        if temp_c > target_temp - hyst_window:
            set_heater(heater, True)
        time.sleep(5)
        set_heater(heater, False)

        time.sleep(3)


if "_main" == __name_:
    temp_loop(25, 20, 67)