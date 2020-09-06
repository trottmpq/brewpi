from datetime import datetime
from flask import current_app

class TempSensorDriver():

    def read(gpio, activeLow=True):
        current_app.logger.info(f"Getting temp from GPIO{gpio}")
        return datetime.now().time().second * (gpio +1)
