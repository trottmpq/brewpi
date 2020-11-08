"""Heater schemas."""
from marshmallow import fields

from brewpi.extensions import ma

from ..models import Kettle
from .heater import HeaterSchema
from .pump import PumpSchema
from .temp_sensor import TempSensorSchema


class KettleSchema(ma.SQLAlchemyAutoSchema):
    """A Heater Schema."""

    class Meta:
        """A Heater Schema Metaclass."""

        model = Kettle

    temp_sensor = fields.Nested(TempSensorSchema, many=False)
    pump = fields.Nested(PumpSchema, many=False)
    heater = fields.Nested(HeaterSchema, many=False)


class KettleStateSchema(ma.Schema):
    """A schema for state in a kettle."""

    state = fields.Bool()


class KettleTempSchema(ma.Schema):
    """A schema for temperature in a kettle."""

    temperature = fields.Float()