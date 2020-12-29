"""Gets / Sets a GPIO on the RPi."""
import RPi.GPIO as GPIO  # noqa


class GpioControl:
    """Raspberry PI GPIO Control Class."""

    def write(number, on, active_low=False):  # noqa
        """Write value to GPIO."""
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(number, GPIO.OUT)
        high = on ^ active_low
        if high:
            GPIO.output(number, GPIO.HIGH)
        else:
            GPIO.output(number, GPIO.LOW)

    def read(number, active_low=False):  # noqa
        """Read value from GPIO."""
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(number, GPIO.IN)

        if GPIO.input(number) == GPIO.HIGH:
            return not active_low
        else:
            return active_low
        #             | AL= False | AL= True  |
        # GPIO HIGH   | True      | False     |
        # GPIO LOW    | False     | True      |
