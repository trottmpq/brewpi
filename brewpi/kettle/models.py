# -*- coding: utf-8 -*-
"""Kettle models."""

from brewpi.database import Column, PkModel, db, reference_col, relationship


class Kettle(PkModel):
    """A Kettle."""

    __tablename__ = "kettles"
    name = Column(db.String(80), unique=True, nullable=False)
    heater_id = reference_col("heaters", nullable=True)
    heater = relationship("Heater", backref="kettles")

    def __init__(self, name, gpio_num, **kwargs):
        """Create instance."""
        super().__init__(name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Kettle({self.name})>"

    def serialize(self):
        """Represent instance as a dict."""
        return {
            "id": self.id,
            "name": self.name
        }
