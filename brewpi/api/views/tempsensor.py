# -*- coding: utf-8 -*-
"""TempSensor API views."""

from brewpi.devices.models import TempSensor
from brewpi.devices.schemas import TempSensorSchema, TempSensorTempSchema

from .baseapi import BaseApi, BaseItemApi


class TempSensorListApi(BaseApi):
    """View for '/api/tempsensor' ."""

    model = TempSensor
    schema = TempSensorSchema()


class TempSensorItemApi(BaseItemApi):
    """/api/tempsensor/<id>."""

    model = TempSensor
    schema = TempSensorSchema()


class TempSensorTempApi(BaseItemApi):
    """/api/tempsensor/<id>/temperature."""

    model = TempSensor
    schema = TempSensorTempSchema()
