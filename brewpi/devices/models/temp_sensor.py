# -*- coding: utf-8 -*-
"""Temperature models."""

from brewpi.database import Column, PkModel, db, relationship


class TempSensor(PkModel):
    """A Temperature Sensor."""

    __tablename__ = "tempsensors"
    name = Column(db.String(80), unique=True, nullable=False)
    gpio_num = Column(db.Integer(), nullable=False)
    temperature = Column(db.Float(), default=False, nullable=False)
    kettle = relationship('Kettle', backref="TempSensor", lazy='dynamic')

    def __init__(self, name, gpio_num, **kwargs):
        """Create instance."""
        super().__init__(name=name, gpio_num=gpio_num, **kwargs)
        self.temperature = 0.0

    @property
    def current_temperature(self):
        """Return the current state."""
        return self.temperature

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<TempSensor({self.name}: {self.gpio_num})>"
