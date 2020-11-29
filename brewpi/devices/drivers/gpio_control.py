"""Gets / Sets a GPIO on the RPi."""
try:
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


except ImportError:
    from flask import current_app

    class GpioControl:
        """Dummy GPIO Control Class."""

        def write(number, on, active_low=False):  # noqa
            """Pretend to write to gpio."""
            if on:
                current_app.logger.info(f"Write output {number} ON\n")
            else:
                current_app.logger.info(f"Write output {number} OFF\n")

        def read(number, active_low=False):  # noqa
            """Pretend to read from gpio."""
            current_app.logger.info(f"Read input {number}\n")
            return not active_low
