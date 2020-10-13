# -*- coding: utf-8 -*-
"""Kettle models."""

from brewpi.database import Column, PkModel, db, relationship


class Kettle(PkModel):
    """A Kettle."""

    __tablename__ = "kettles"
    name = Column(db.String(80), unique=True, nullable=False)
    temp_sensor = relationship("TempSensor", back_populates="kettle", uselist=False)
    pump = relationship("Pump", back_populates="kettle", uselist=False)
    heater = relationship("Heater", back_populates="kettle")

    def __init__(self, name, **kwargs):
        """Create instance."""
        super().__init__(name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Kettle({self.name})>"
