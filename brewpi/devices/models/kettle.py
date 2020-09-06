# -*- coding: utf-8 -*-
"""Kettle models."""

from brewpi.database import Column, PkModel, db, reference_col, relationship


class Kettle(PkModel):
    """A Kettle."""

    __tablename__ = "kettles"
    name = Column(db.String(80), unique=True, nullable=False)
    heater = relationship("Heater", back_populates="kettle")
    heater_id = reference_col("heaters", nullable=True)
    tempsense = relationship("TempSensor", back_populates="kettle")
    tempsense_id = reference_col("tempsensors", nullable=True)
    pump = relationship("Pump", back_populates="kettle")
    pump_id = reference_col("pump", nullable=True)
    
    def __init__(self, name, **kwargs):
        """Create instance."""
        super().__init__(name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Kettle({self.name})>"
