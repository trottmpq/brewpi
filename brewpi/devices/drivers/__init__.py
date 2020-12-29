"""Hardware drivers for control of raspbery pi."""
try:
    from .gpio_control import GpioControl  # noqa
except ImportError:
    from .dummy_gpio_control import GpioControl  # noqa

try:
    from .temp_sensor import TempSensorDriver, TempSensorHAL, save_temp_to_file  # noqa
except ImportError:
    from .dummy_temp_sensor import TempSensorDriver, save_temp_to_file  # noqa
