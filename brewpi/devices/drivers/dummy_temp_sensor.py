"""Temp Sensor Driver. If we aren't on an RPi, this module still provides dummy data for testing."""
import math
import time


class TempSensorDriver:
    """Dummy Temp Sensor Driver."""

    def get_temp_c(gpio):
        """Get Temperature in degrees Celcius."""
        max = 100

        seconds = time.time()
        temp_sin = math.sin(seconds * 2 * math.pi / 60 / (gpio + 1)) + 1
        return "{:.2f}".format(round(temp_sin * max / 2, 2))


def save_temp_to_file():
    """Dummy method."""
    pass
