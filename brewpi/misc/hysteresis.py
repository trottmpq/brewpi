#!python

import argparse
import requests
import time

def get_temp(kettle_id):
    resp = requests.get(f'http://localhost:5000/devices/Kettle/{kettle_id}/temperature')
    return resp.json().get("temperature")

def get_targettemp(kettle_id):
    resp = requests.get(f'http://localhost:5000/devices/Kettle/{kettle_id}/targettemp')
    return resp.json().get("temperature")

def set_heater(kettle_id, onoff):
    if(onoff):
        print("Heater ON")
    else:
        print("Heater OFF")
    requests.put(f'http://127.0.0.1:5000/devices/Kettle/{kettle_id}/heaterstate', json={'state': onoff})

def get_hyst_window(kettle_id):
    resp = requests.get(f'http://localhost:5000/devices/Kettle/{kettle_id}')
    return resp.json().get("hyst_window")

def temp_loop(kettle_id):
    """Hysterises loop to turn hold the kettle as a set temperature."""
    heaterOn = False
    while True:
        temp_c = get_temp(kettle_id)  # Current temperature
        target_temp = get_targettemp(kettle_id)
        hyst_window = get_hyst_window(kettle_id)
        
        print(f"{temp_c},{target_temp},{hyst_window},")
        if heaterOn:
            if temp_c > (target_temp + hyst_window):
                heaterOn = False
                set_heater(kettle_id, heaterOn)
        else:
            if temp_c < (target_temp - hyst_window):
                heaterOn = True
                set_heater(kettle_id, heaterOn)
        time.sleep(5)

if "__main__" == __name__:
<<<<<<< HEAD
    temp_loop(3)
=======
    # Create the parser
    my_parser = argparse.ArgumentParser(description='hysteresis loop for a kettle')

    # Add the arguments
    my_parser.add_argument('kettle_id', type=int, help='id of kettle in the db')

    # Execute parse_args()
    args = my_parser.parse_args()
    temp_loop(args.kettle_id)
>>>>>>> argparse for loop
