"""Heater schemas."""
from marshmallow import fields

from brewpi.extensions import ma

from ..models import Kettle
from .heater import HeaterSchema
from .pump import PumpSchema
from .temp_sensor import TempSensorSchema


class KettleSchema(ma.SQLAlchemySchema):
    """A Heater Schema."""

    class Meta:
        """A Heater Schema Metaclass."""

        model = Kettle

    id = ma.auto_field()
    name = ma.auto_field()
    temp_sensor = fields.Nested(TempSensorSchema, many=False)
    pump = fields.Nested(PumpSchema, many=False)
    heater = fields.Nested(HeaterSchema, many=False)
