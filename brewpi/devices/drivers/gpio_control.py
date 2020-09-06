#Gets / Sets a GPIO on the RPi
from flask import current_app

class GpioControl:
    def write(number, on, activeLow=False):
        high = on ^ activeLow
        if high:
            current_app.logger.info("Setting gpio{} high".format(number))
        else:
            current_app.logger.info("Setting gpio{} low".format(number))
        pass

    def read(number, activeLow=False):
        current_app.logger.info("Reading gpio{}".format(number))
        return not activeLow