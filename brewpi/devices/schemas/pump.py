"""Pump schemas."""

from brewpi.extensions import ma

from ..models import Pump


class PumpSchema(ma.SQLAlchemyAutoSchema):
    """A Pump Schema."""

    class Meta:
        """A Pump Schema Metaclass."""

        model = Pump


class PumpStateSchema(ma.SQLAlchemyAutoSchema):
    """A Pump Schema."""

    class Meta:
        """A Pump Schema Metaclass."""

        model = Pump
        fields = ["state"]
