"""Gets / Sets a GPIO on the RPi."""
try:
    import RPi.GPIO as GPIO # noqa

    class GpioControl:
        """Raspberry PI GPIO Control Class."""

        def write(self, number, on, active_low=False):
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(number, GPIO.OUT)
            high = on ^ active_low
            if high:
                GPIO.output(number, GPIO.HIGH)
            else:
                GPIO.output(number, GPIO.LOW)

        def read(self, number, active_low=False):
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


except ImportError:
    from flask import current_app

    class GpioControl:
        """Dummy GPIO Control Class."""

        def write(self, number, on, active_low=False):
            if on:
                current_app.logger.info(f"Write output {number} ON\n")
            else:
                current_app.logger.info(f"Write output {number} OFF\n")

        def read(self, number, active_low=False):
            print(f"Read input {number}\n")
            return not active_low
