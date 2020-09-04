"""Heater schemas."""

from brewpi.extensions import ma

from ..models import Heater


class HeaterSchema(ma.SQLAlchemyAutoSchema):
    """A Heater Schema."""

    class Meta:
        """A Heater Schema Metaclass."""

        model = Heater
