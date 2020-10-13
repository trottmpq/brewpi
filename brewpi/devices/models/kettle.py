# -*- coding: utf-8 -*-
"""Kettle models."""

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

    def __init__(self, name, **kwargs):
        """Create instance."""
        super().__init__(name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Kettle({self.name})>"

    def current_temp(self):
        if self.temp_sensor:
            self.temp_sensor.update()
            return self.temp_sensor.current_temperature

    def heater_enable(self, state):
        if self.heater:
            if state:
                self.heater.turn_on()
            else:
                self.heater.turn_off()

    def pump_enable(self, state):
        if self.pump:
            if state:
                self.pump.turn_on()
            else:
                self.pump.turn_off()
