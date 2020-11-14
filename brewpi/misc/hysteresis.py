#!python

import requests
import time

def get_temp(kettle_id):
    resp = requests.get(f'http://localhost:5000/devices/Kettle/{kettle_id}/temperature')
    return resp.json().get("temperature")

def get_targettemp(kettle_id):
    resp = requests.get(f'http://localhost:5000/devices/Kettle/{kettle_id}/targettemp')
    return resp.json().get("temperature")

def set_heater(kettle_id, onoff):
    requests.put(f'http://127.0.0.1:5000/devices/Kettle/{kettle_id}/heaterstate', json={'state': onoff})

def get_hyst_window(kettle_id):
    resp = requests.get(f'http://localhost:5000/devices/Kettle/{kettle_id}')
    return resp.json().get("hyst_window")

def temp_loop(kettle_id):
    """Hysterises loop to turn hold the kettle as a set temperature."""
    while True:
        temp_c = get_temp(kettle_id)  # Current temperature
        target_temp = get_targettemp(kettle_id)
        hyst_window = get_hyst_window(kettle_id)
        print(f"temp is {temp_c} aiming for {target_temp}+/-{hyst_window}")
        if temp_c > target_temp + hyst_window:
            set_heater(kettle_id, False)
        if temp_c > target_temp - hyst_window:
            set_heater(kettle_id, True)
        time.sleep(5)
        # set_heater(kettle_id, False)

        # time.sleep(3)


if "__main__" == __name__:
    temp_loop(1)
