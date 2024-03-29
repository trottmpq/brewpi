# -*- coding: utf-8 -*-
"""Heater models."""

from brewpi.database import Column, PkModel, db, relationship
from brewpi.devices.drivers import GpioControl


class Heater(PkModel):
    """A Heater."""

    __tablename__ = "heaters"
    name = Column(db.String(80), unique=True, nullable=False)
    gpio_num = Column(db.Integer(), nullable=False)
    state = Column(db.Boolean(), default=False, nullable=False)
    active_low = Column(db.Boolean(), default=False, nullable=False)
    kettle = relationship("Kettle", back_populates="heater")

    def __init__(self, name, gpio_num, **kwargs):
        """Create instance."""
        super().__init__(name=name, gpio_num=gpio_num, **kwargs)

    def turn_on(self):
        """Turn heater on."""
        self.state = True
        GpioControl.write(self.gpio_num, True, self.active_low)
        self.update()

    def turn_off(self):
        """Turn heater off."""
        self.state = False
        GpioControl.write(self.gpio_num, False, self.active_low)
        self.update()

    @property
    def current_state(self):
        """Return the current state."""
        return self.state

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Heater({self.name}: {self.gpio_num}, {self.state})>"
