#!python

import argparse
import time

import requests


def get_temp(kettle_id):
    resp = requests.get(
        f"http://localhost:5000/api/devices/Kettle/{kettle_id}/temperature"
    )
    return resp.json().get("temperature")


def get_targettemp(kettle_id):
    resp = requests.get(
        f"http://localhost:5000/api/devices/Kettle/{kettle_id}/targettemp"
    )
    return resp.json().get("temperature")


def set_heater(kettle_id, onoff):
    if onoff:
        print("Heater ON")
    else:
        print("Heater OFF")
    requests.put(
        f"http://127.0.0.1:5000/api/devices/Kettle/{kettle_id}/heaterstate",
        json={"state": onoff},
    )


def get_hyst_window(kettle_id):
    resp = requests.get(f"http://localhost:5000/api/devices/Kettle/{kettle_id}")
    return resp.json().get("hyst_window")


def temp_loop(hlt_kettle_id, mash_kettle_id):
    """Hysterises loop to turn hold the kettle as a set temperature."""
    heaterOn = False
    while True:
        hlt_temp_c = get_temp(hlt_kettle_id)  # Current temperature
        mash_temp_c = get_temp(mash_kettle_id)  # Current temperature
        target_temp = get_targettemp(mash_kettle_id)
        hyst_window = get_hyst_window(mash_kettle_id)

        print(f"Mash Kettle: {mash_temp_c},{target_temp},{hyst_window}")
        print(f"HLT Kettle:{hlt_temp_c}")
        if abs(mash_temp_c - hlt_temp_c) > 5:
            print("SLOW THE FLOW")

        if heaterOn:
            if mash_temp_c > (target_temp + hyst_window):
                heaterOn = False
                set_heater(mash_kettle_id, heaterOn)
        else:
            if mash_temp_c < (target_temp - hyst_window):
                heaterOn = True
                set_heater(mash_kettle_id, heaterOn)
        time.sleep(5)


if "__main__" == __name__:
    # Create the parser
    my_parser = argparse.ArgumentParser(description="hysteresis loop for a kettle")

    # Add the arguments
    my_parser.add_argument("hlt_kettle_id", type=int, help="id of HLT kettle in the db")
    my_parser.add_argument(
        "mash_kettle_id", type=int, help="id of Mash kettle in the db"
    )

    # Execute parse_args()
    args = my_parser.parse_args()
    temp_loop(args.hlt_kettle_id, args.mash_kettle_id)
