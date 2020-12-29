"""Gets / Sets a GPIO on the RPi."""
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
