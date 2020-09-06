# -*- coding: utf-8 -*-
"""Temperature models."""

from brewpi.database import Column, PkModel, db, relationship


from brewpi.devices.drivers.temp_sensor import TempSensorDriver
class TempSensor(PkModel):
    """A Temperature Sensor."""

    __tablename__ = "tempsensors"
    name = Column(db.String(80), unique=True, nullable=False)
    gpio_num = Column(db.Integer(), nullable=False)
    activeLow = Column(db.Boolean(), default=True, nullable=False)
    temperature = Column(db.Float(), default=False, nullable=False)
    kettle = relationship("Kettle", backref="TempSensor", lazy="dynamic")

    def __init__(self, name, gpio_num, **kwargs):
        """Create instance."""
        super().__init__(name=name, gpio_num=gpio_num, **kwargs)
        self.temperature = 0.0

    @property
    def current_temperature(self):
        """Return the current state."""
        return self.temperature

    def update(self):
        self.temperature = TempSensorDriver.read(self.gpio_num, self.activeLow)
        self.save()

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<TempSensor({self.name}: {self.gpio_num})>"
