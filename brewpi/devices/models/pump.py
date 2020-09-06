# -*- coding: utf-8 -*-
"""Pump models."""

from brewpi.database import Column, PkModel, db, relationship

from brewpi.devices.drivers.gpio_control import GpioControl

class Pump(PkModel):
    """A Pump."""

    __tablename__ = "pump"
    name = Column(db.String(80), unique=True, nullable=False)
    gpio_num = Column(db.Integer(), nullable=False)
    state = Column(db.Boolean(), default=False, nullable=False)
    activeLow = Column(db.Boolean(), default=False, nullable=False)
    kettle = relationship("Kettle", backref="Pump", lazy="dynamic")

    def __init__(self, name, gpio_num, **kwargs):
        """Create instance."""
        super().__init__(name=name, gpio_num=gpio_num, **kwargs)
        self.state = False

    def turn_on(self):
        """Turn Pump on."""
        self.state = True
        GpioControl.write(self.gpio_num, True, self.activeLow)

    def turn_off(self):
        """Turn Pump off."""
        self.state = False
        GpioControl.write(self.gpio_num, False, self.activeLow)

    def update(self):
        if self.state:
            self.turn_on()
        else:
            self.turn_off()
    @property
    def current_state(self):
        """Return the current state."""
        return self.state

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Pump({self.name}: {self.gpio_num}, {self.state})>"