#!python
"""Helper function for turning the heater on and off."""
# myls.py
# Import the argparse library
import argparse

import requests


def set_heater(kettle_id, onoff):
    """Send heater request."""
    requests.put(
        f"http://127.0.0.1:5000/api/devices/Kettle/{kettle_id}/heaterstate",
        json={"state": onoff},
    )


def str2bool(v):
    """Convert string to boolean."""
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


if "__main__" == __name__:
    # Create the parser
    my_parser = argparse.ArgumentParser(description="Turn a heater on or off")

    # Add the arguments
    my_parser.add_argument(
        "kettle_id", type=int, help="id of kettle the heater is attached to in the db"
    )
    my_parser.add_argument("onoff", type=str2bool, help="on = true, off = false")

    # Execute parse_args()
    args = my_parser.parse_args()

    print(f"Turning kettle {args.kettle_id}'s heater {args.onoff}")

    set_heater(args.kettle_id, args.onoff)
