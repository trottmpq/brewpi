# -*- coding: utf-8 -*-
"""Kettle models."""
import threading
import time

from flask import current_app

from brewpi.database import Column, PkModel, db, relationship


class Kettle(PkModel):
    """A Kettle."""

    __tablename__ = "kettles"
    name = Column(db.String(80), unique=True, nullable=False)
    target_temp = Column(db.Float(), default=0.0)
    is_running = Column(db.Boolean(), default=False, nullable=False)
    hyst_window = Column(db.Float(), default=5.0)

    temp_sensor = relationship("TempSensor", back_populates="kettle", uselist=False)
    pump = relationship("Pump", back_populates="kettle", uselist=False)
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

    def hysteresis_loop(self):
        """Hysterises loop to turn hold the kettle as a set temperature."""
        t = threading.currentThread()
        while getattr(t, "is_running", True):
            temp_c = self.current_temp()  # Current temperature

            if temp_c + self.hyst_window < self.target_temp:
                self.heater_enable(True)
            if temp_c - self.hyst_window < self.target_temp:
                self.heater_enable(False)
            time.sleep(5)
        self.heater_enable(False)

    def thread_function(self):
        """Dummy function to prove threading."""
        t = threading.currentThread()
        while getattr(t, "is_running", True):
            print("running")
            time.sleep(2)
        print("stopping")

    def start_loop(self):
        """Start Thread if not already active."""
        # Creat thread if doesn't already exist.
        if not current_app.threads.get(f"{self.name}_id"):
            current_app.threads[f"{self.name}_id"] = threading.Thread(
                target=self.thread_function
            )
        if not current_app.threads[f"{self.name}_id"].is_alive():
            current_app.logger.info(f"{self.name}_id starting")
            current_app.threads[f"{self.name}_id"].start()
            self.is_running = True
            self.update()
            return
        current_app.logger.info(f"{self.name}_id is already running")

    def stop_loop(self):
        """Stop Thread if not already stopped."""
        if current_app.threads.get(f"{self.name}_id"):
            current_app.logger.info("Thread: about to stop")
            self.is_running = False
            current_app.threads[f"{self.name}_id"].is_running = False
            current_app.threads[f"{self.name}_id"].join()
            if not current_app.threads[f"{self.name}_id"].is_alive():
                del current_app.threads[f"{self.name}_id"]
            self.update()
        else:
            current_app.logger.info("thread has already stopped")
