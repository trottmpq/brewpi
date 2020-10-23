# -*- coding: utf-8 -*-
"""Kettle models."""
import threading
import time

from brewpi.database import Column, PkModel, db, relationship


class Kettle(PkModel):
    """A Kettle."""

    __tablename__ = "kettles"
    name = Column(db.String(80), unique=True, nullable=False)
    target_temp = Column(db.Float(), default=0.0)
    state = Column(db.Boolean(), default=False, nullable=False)
    temp_sensor = relationship("TempSensor", back_populates="kettle", uselist=False)
    pump = relationship("Pump", back_populates="kettle", uselist=False)
    heater = relationship("Heater", back_populates="kettle", uselist=False)

    hyst_window = 5.0

    def __init__(self, name, **kwargs):
        """Create instance."""
        super().__init__(name=name, **kwargs)
        self.control_loop = threading.Thread(target=self.hysteresis_loop)

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

    def hysteresis_loop(self):
        """Hysterises loop to turn hold the kettle as a set temperature."""
        while self.is_running:
            temp_c = self.current_temp()  # Current temperature

            if self.heater.state is True:
                if temp_c > self.target_temp + self.hyst_window:
                    self.heater_enable(False)
            if self.heater.state is False:
                if temp_c < self.target_temp - self.hyst_window:
                    self.heater_enable(True)
            time.sleep(5)
