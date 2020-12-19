"""Celery tasks to be spawned."""
import time

from flask import current_app

from brewpi.extensions import celery

from .. import models
from ..drivers import temp_sensor


@celery.task
def add(x, y, kettle_id):
    """Example task."""
    # db_sess = db.session
    current_app.logger.info(f"add {x} and {y}")
    kettle = models.Kettle.get_by_id(kettle_id)
    current_app.logger.info(f"kettle name is {kettle.name}")
    while True:
        time.sleep(5)
        current_app.logger.info(f"kettle loop state:{kettle.is_running}")
        kettle = models.Kettle.get_by_id(kettle_id)
        current_app.logger.info(f"kettle loop state:{kettle.is_running}")

    # return x + y


@celery.task
def hysteresis_loop(kettle_id):
    """Hysterises loop to turn hold the kettle as a set temperature."""
    kettle = models.Kettle.get_by_id(kettle_id)
    heater = models.Heater.get_by_id(kettle.heater_id)
    while True:
        temp_c = kettle.current_temp()  # Current temperature
        current_app.logger.info(f"kettle current temp:{temp_c}")
        current_app.logger.info(f"kettle target temp:{kettle.target_temp}")
        current_app.logger.info(f"kettle hyst window:{kettle.hyst_window}")

        current_app.logger.info(f"kettle heater state:{kettle.heater.current_state}")
        heater_state = kettle.heater.current_state
        if heater_state:
            if temp_c > (kettle.target_temp + kettle.hyst_window):
                heater.turn_off()
                heater_state = False
                current_app.logger.info("Turning OFF")
        else:
            if temp_c < (kettle.target_temp - kettle.hyst_window):
                heater.turn_on()
                heater_state = True
                current_app.logger.info("Turning ON")
        time.sleep(5)

    # def pid_loop(self):
    #     """PID Loop. Values are from craftbeerpi which are roughly the same as ours. hopefully ok?."""
    #     p = 44
    #     i = 165
    #     d = 4
    #     sample_time = 5
    #     pid = simple_pid.PID(
    #         p, i, d, setpoint=self.target_temp
    #     )  # dont think this can be changed once started.
    #     pid.output_limits = (0, 100)
    #     pid.sample_time = sample_time

    #     while kettle.is_loop_running:
    #         heat_percent = pid(self.current_temp())
    #         heating_time = pid.sample_time * (heat_percent / 100)
    #         wait_time = pid.sample_time - heating_time
    #         self.heater_enable(True)
    #         time.sleep(heating_time)
    #         self.heater_enable(False)
    #         time.sleep(wait_time)
    #     self.heater_enable(False)


@celery.task
def update_temperature():
    temp_sensor.save_temp_to_file()
