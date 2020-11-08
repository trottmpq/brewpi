"""Temp Sensor Driver. If we aren't on an RPi, this module still provides dummy data for testing."""
import math

from flask import current_app

try:
    import RPi.GPIO as GPIO  # noqa
    import spidev

    class TempSensorDriver:
        """SPI Temp Sensor Driver."""

        _MAX31865_CONFIG_REG = 0x00
        REG_RTD_MSB = 0x01
        REG_RTD_LSB = 0x02
        REG_HIFLT_MSB = 0x03
        REG_HIFLT_LSB = 0x04
        REG_LOFLT_MSB = 0x05
        REG_LOFLT_LSB = 0x06
        REG_FLT_STATUS = 0x07

        WRITE_FLAG = 0x80

        RREF = 430.0  # reference resistor in Ohms
        RTD_NOM = 100
        CONFIG = 0xD1

        def __init__(self, gpio_number, active_low=True):
            """Initialise SPI Chip."""
            self.gpio_number = gpio_number
            self.active_low = active_low
            if self.gpio_number:
                GPIO.setwarnings(False)
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(self.gpio_number, GPIO.OUT)
                self.chip_select(False)

            self.write_spi(self._MAX31865_CONFIG_REG, [self.CONFIG])  # set up device
            r = self.read_spi(self._MAX31865_CONFIG_REG, 1)[0]  # read config back
            if r != self.CONFIG:
                current_app.logger.error("Error setting config")

        def chip_select(self, select):
            """Set chip select if not normal SPI CS."""
            if self.gpio_number:  # 0 or none, rely on normal SPI CS
                if select == self.active_low:
                    en = GPIO.LOW
                else:
                    en = GPIO.HIGH
                GPIO.output(self.gpio_number, en)  # enable

        def read_spi(self, reg, length):
            """Read."""
            rtd = spidev.SpiDev()
            rtd.open(0, 0)
            rtd.max_speed_hz = 5000
            rtd.mode = 1
            d = [0] * (length + 1)
            d[0] = reg
            self.chip_select(True)
            r = rtd.xfer2(d)
            self.chip_select(False)
            rtd.close()
            return r[1:]

        def write_spi(self, reg, data):
            """Write."""
            rtd = spidev.SpiDev()
            rtd.open(0, 0)
            rtd.max_speed_hz = 5000
            rtd.mode = 1
            d = list()
            d.append(reg + self.WRITE_FLAG)
            d.extend(data)
            self.chip_select(True)
            rtd.xfer2(d)
            self.chip_select(False)
            rtd.close()
            return

        def get_resistance(self):
            """Get the measured resistance."""
            r = self.read_spi(self.REG_RTD_MSB, 2)
            rtdval = r[0] * 256 + r[1]
            if (rtdval % 2) == 1:  # lowest bit is a fault flag
                r = self.read_spi(self.REG_FLT_STATUS, 1)[0]
                current_app.logger.error("Error 0x{:02x} detected".format(r))
                self.write_spi(
                    self._MAX31865_CONFIG_REG, [self.CONFIG + 2]
                )  # clear fault
                # if fault is cleared, should read okay next time.
                r = self.read_spi(self.REG_RTD_MSB, 2)
                rtdval = r[0] * 256 + r[1]
            rtdval >>= 1  # remove the Fault bit
            rtdval /= 32768
            rtdval *= self.RREF
            return rtdval

        def get_temp_c(self):
            """Get Temperature in degrees Celcius."""
            # This maths originates from:
            # http://www.analog.com/media/en/technical-documentation/application-notes/AN709_0.pdf

            rtd_a = 3.9083e-3
            rtd_b = -5.775e-7

            z1 = -rtd_a
            z2 = math.pow(rtd_a, 2) - (4 * rtd_b)
            z3 = (4 * rtd_b) / self.RTD_NOM
            z4 = 2 * rtd_b

            raw_reading = self.get_resistance()
            temp = (z1 + math.sqrt(z2 + (z3 * raw_reading))) / z4
            if temp <= 0:
                # If temp is negative the above is invalid. 2nd order eq is
                # accurate to +0.075°C/–0.17°C. Easily good enough for what we
                # need. For the following maths to work, nominal RTD resistance
                # must be normalized to 100 ohms.
                raw_reading /= self.RTD_NOM
                raw_reading *= 100
                temp = -242.02
                temp += 2.2228 * raw_reading
                temp += 2.5859e-3 * math.pow(raw_reading, 2)
            return round(temp, 2)


except ImportError:
    from datetime import datetime

    class TempSensorDriver:
        """Dummy Temp Sensor Driver."""

        def __init__(self, gpio_number, active_low):
            """Initialise Temp Sensor Driver."""
            self.gpio = gpio_number
            self.active_low = active_low

        def get_temp_c(self):
            """Get Temperature in degrees Celcius."""
            max = 100
            n = datetime.now().time()
            seconds = float(n.second) + float(n.microsecond) / 1000000.0
            temp_sin = math.sin(seconds * 2 * math.pi / 60 / (self.gpio + 1))
            return "{:.2f}".format(round(temp_sin * max / 2, 2))


if "__main__" == __name__:
    temp_sensor = TempSensorDriver(0)
    print(temp_sensor.get_resistance())
    print(temp_sensor.get_temp_c())
