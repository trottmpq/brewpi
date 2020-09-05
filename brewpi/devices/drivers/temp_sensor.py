from datetime import datetime

class TempSensorDriver():

    def temperature(id):
        return datetime.now().time().second * (id +1)
