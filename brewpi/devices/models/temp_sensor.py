# -*- coding: utf-8 -*-
"""Temperature models."""

from brewpi.database import Column, PkModel, db, relationship
from brewpi.devices.drivers.temp_sensor import TempSensorDriver


class TempSensor(PkModel):
    """A Temperature Sensor."""

    __tablename__ = "tempsensors"
    name = Column(db.String(80), unique=True, nullable=False)
    gpio_num = Column(db.Integer(), nullable=False)
    active_low = Column(db.Boolean(), default=True, nullable=False)
    temperature = Column(db.Float(), default=False, nullable=False)
    kettle_id = Column(db.Integer(), db.ForeignKey("kettles.id"), nullable=True)
    kettle = relationship("Kettle", back_populates="temp_sensor")

    def __init__(self, name, gpio_num, **kwargs):
        """Create instance."""
        super().__init__(name=name, gpio_num=gpio_num, **kwargs)
        self.temperature = 0.0
        # self.temp_sensor = TempSensorDriver(self.gpio_num, self.active_low)

    @property
    def current_temperature(self):
        """Return the current temperature."""
        self.temperature = TempSensorDriver(self.gpio_num, self.active_low).get_temp_c()
        self.save()
        return self.temperature

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<TempSensor({self.name}: {self.gpio_num})>"
