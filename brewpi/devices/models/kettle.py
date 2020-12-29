# -*- coding: utf-8 -*-
"""Kettle models."""
import enum

# import simple_pid
from flask import current_app

from brewpi.database import Column, PkModel, db, relationship

from ..tasks import hysteresis_loop, pwm_loop


class Kettle(PkModel):
    """A Kettle."""

    class ControlType(enum.Enum):
        """Enum for types of control."""

        PWM = 1
        HYSTERESIS = 2
        PID = 3

    __tablename__ = "kettles"
    name = Column(db.String(80), unique=True, nullable=False)
    target_temp = Column(db.Float(), default=0.0)
    is_running = Column(db.Boolean(), default=False, nullable=False)
    hyst_window = Column(db.Float(), default=5.0)
    control_type = Column(db.Enum(ControlType), default=ControlType.HYSTERESIS)

    temp_sensor = relationship("TempSensor", back_populates="kettle", uselist=False)
    pump = relationship("Pump", back_populates="kettle", uselist=False)

    heater_id = Column(db.Integer(), db.ForeignKey("heaters.id"), nullable=True)
    heater = relationship("Heater", back_populates="kettle", uselist=False)

    task_id = Column(db.String(40), nullable=True)

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

    @property
    def is_loop_running(self):
        """Return the status of the control loop."""
        return self.is_running

    @is_loop_running.setter
    def is_loop_running(self, value):
        """Set is loop running."""
        self.is_running = value
        self.update()

    def start_loop(self):
        """Start Thread if not already active."""
        self.is_loop_running = True
        if self.control_type == self.ControlType.HYSTERESIS:
            task = hysteresis_loop.delay(self.id)
            self.task_id = task.id
            self.update()
        else:
            task = pwm_loop.delay(self.id)
            self.task_id = task.id
            self.update()

        current_app.logger.info(f"thread id: {task.id}")
        current_app.logger.info(f"thread status: {task.status}")
        current_app.logger.info(f"thread type: {self.control_type}")

    def stop_loop(self):
        """Stop Thread if not already stopped."""
        hysteresis_loop.AsyncResult(self.task_id).revoke(terminate=True)
        self.is_loop_running = False
        self.heater_enable(False)
        current_app.logger.info("thread has stopped")
