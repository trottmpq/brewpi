"""Temp Sensor Driver. If we aren't on an RPi, this module still provides dummy data for testing."""
import math
import pickle

import RPi.GPIO as GPIO  # noqa
import spidev


class TempSensorHAL:
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

    def init(self):
        """Init the MAX31865."""
        if self.gpio_number:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.gpio_number, GPIO.OUT)
            self.chip_select(False)

        self.write_spi(self._MAX31865_CONFIG_REG, [self.CONFIG])  # set up device
        r = self.read_spi(self._MAX31865_CONFIG_REG, 1)[0]  # read config back
        if r != self.CONFIG:
            print("Error setting config")
        self.write_spi(self.REG_HIFLT_MSB, [0xFF])
        self.write_spi(self.REG_HIFLT_LSB, [0xFF])
        self.write_spi(self.REG_LOFLT_MSB, [0])
        self.write_spi(self.REG_LOFLT_LSB, [0])

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
            print("Error 0x{:02x} detected".format(r))
            self.write_spi(self._MAX31865_CONFIG_REG, [self.CONFIG + 2])  # clear fault
            # if fault is cleared, should read okay next time.
            r = self.read_spi(self.REG_RTD_MSB, 2)
            rtdval = r[0] * 256 + r[1]
        rtdval >>= 1  # remove the Fault bit
        rtdval /= 32768
        rtdval *= self.RREF
        return rtdval

    def read_temp_c(self):
        """Get Temperature in degrees Celcius."""
        # This maths originates from:
        # http://www.analog.com/media/en/technical-documentation/application-notes/AN709_0.pdf

        rtd_a = 3.9083e-3
        rtd_b = -5.775e-7

        z1 = -rtd_a
        z2 = math.pow(rtd_a, 2) - (4 * rtd_b)
        z3 = (4 * rtd_b) / self.RTD_NOM
        z4 = 2 * rtd_b
        try:
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
            if temp < 0 or temp > 100:
                return -1
            print(f"Gpio={self.gpio_number} Temperature= {temp} ")
            return round(temp, 2)
        except:
            print("Failed to read temperature")
            self.init()
            return -1


def save_temp_to_file():
    """Save temp readings to a file."""
    t16 = TempSensorHAL(16, True)
    t16.init()
    t19 = TempSensorHAL(19, True)
    t19.init()
    t20 = TempSensorHAL(20, True)
    t20.init()
    temps = dict()
    temps["16"] = t16.read_temp_c()
    temps["19"] = t19.read_temp_c()
    temps["20"] = t20.read_temp_c()
    with open("temps.p", "wb") as fp:
        pickle.dump(temps, fp, protocol=pickle.HIGHEST_PROTOCOL)


class TempSensorDriver:
    """Driver class to retrieve temp from file."""

    def get_temp_c(gpio):
        """Get temp from file if available."""
        try:
            with open("temps.p", "rb") as fp:
                temps = pickle.load(fp)
                temp = temps.get(str(gpio))
                if temp:
                    return temp
                else:
                    return 0
        except FileNotFoundError:
            return 0
