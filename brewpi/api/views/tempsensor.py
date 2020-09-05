# -*- coding: utf-8 -*-
"""TempSensor API views."""

from brewpi.devices.models import TempSensor
from brewpi.devices.schemas import TempSensorSchema, TempSensorTempSchema

from .baseapi import ListApi, ModelApi, ReadOnlyApi


class TempSensorListApi(ListApi):
    """View for '/api/tempsensor' ."""

    model = TempSensor
    schema = TempSensorSchema()


class TempSensorItemApi(ModelApi):
    """/api/tempsensor/<id>."""

    model = TempSensor
    schema = TempSensorSchema()


class TempSensorTempApi(ReadOnlyApi):
    """/api/tempsensor/<id>/temperature."""

    model = TempSensor
    schema = TempSensorTempSchema()
