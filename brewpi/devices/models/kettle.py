# -*- coding: utf-8 -*-
"""Kettle models."""
# import time

# import simple_pid
from flask import current_app

from brewpi.database import Column, PkModel, db, relationship

from ..tasks import add


class Kettle(PkModel):
    """A Kettle."""

    __tablename__ = "kettles"
    name = Column(db.String(80), unique=True, nullable=False)
    target_temp = Column(db.Float(), default=0.0)
    is_running = Column(db.Boolean(), default=False, nullable=False)
    hyst_window = Column(db.Float(), default=5.0)

    temp_sensor = relationship("TempSensor", back_populates="kettle", uselist=False)
    pump = relationship("Pump", back_populates="kettle", uselist=False)

    heater_id = Column(db.Integer(), db.ForeignKey("heaters.id"), nullable=True)
    heater = relationship("Heater", back_populates="kettle", uselist=False)

    def __init__(self, name, **kwargs):
        """Create instance."""
        super().__init__(name=name, **kwargs)
        # self.control_loop = threading.Thread(target=self.hysteresis_loop)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Kettle({self.name})>"

    def current_temp(self):
        """Get current temp of kettle."""
        if self.temp_sensor:
            return self.temp_sensor.current_temperature

    def heater_enable(self, state):
        """Turn heater in kettle on or off."""
        if self.heater:
            if state:
                self.heater.turn_on()
            else:
                self.heater.turn_off()

    def pump_enable(self, state):
        """Turn pump in kettle on or off."""
        if self.pump:
            if state:
                self.pump.turn_on()
            else:
                self.pump.turn_off()

    @property
    def current_target_temperature(self):
        """Return the current temperature."""
        return self.target_temp

    @current_target_temperature.setter
    def current_target_temperature(self, value):
        """Return the current temperature."""
        self.target_temp = value
        self.update()

    # def hysteresis_loop(self):
    #     """Hysterises loop to turn hold the kettle as a set temperature."""
    #     t = threading.currentThread()
    #     while getattr(t, "is_running", True):
    #         temp_c = self.current_temp()  # Current temperature

    #         if temp_c + self.hyst_window < self.target_temp:
    #             self.heater_enable(True)
    #         if temp_c - self.hyst_window < self.target_temp:
    #             self.heater_enable(False)
    #         time.sleep(5)
    #     self.heater_enable(False)

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

    #     t = threading.currentThread()
    #     while getattr(t, "is_running", True):
    #         heat_percent = pid(self.current_temp())
    #         heating_time = pid.sample_time * (heat_percent / 100)
    #         wait_time = pid.sample_time - heating_time
    #         self.heater_enable(True)
    #         time.sleep(heating_time)
    #         self.heater_enable(False)
    #         time.sleep(wait_time)
    #     self.heater_enable(False)

    # def thread_function(self):
    #     """Dummy function to prove threading."""
    #     while self.is_running:
    #         current_app.logger.info("running")
    #         time.sleep(5)
    #     print("stopping")

    def start_loop(self):
        """Start Thread if not already active."""
        future = add.delay(1, 2, 1)
        # self.is_running = future.running()
        # current_app.logger.info(f"thread dir: {dir(future)}")
        current_app.logger.info(f"thread id: {future.id}")
        current_app.logger.info(f"thread status: {future.status}")
        # current_app.logger.info(f"thread result: {future.result()}")

        current_app.logger.info(f"thread answer: {future.get(timeout=1)}")
        # future.start(4, 5)
        # current_app.logger.info(f"thread answer: {future.get(timeout=1)}")
        # current_app.logger.info(f"thread running: {future.running()}")
        # current_app.logger.info(f"thread {future.result(timeout=1)}")
        return

    def stop_loop(self, future):
        """Stop Thread if not already stopped."""
        future.cancel()
        self.is_running = future.is_running()
        current_app.logger.info("thread has already stopped")
