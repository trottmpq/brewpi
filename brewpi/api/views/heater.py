# -*- coding: utf-8 -*-
"""Heater API views."""

from brewpi.devices.models import Heater
from brewpi.devices.schemas import HeaterSchema, HeaterStateSchema

from .baseapi import ListApi, ModelApi


class HeaterListApi(ListApi):
    """View for '/api/heater' ."""

    model = Heater
    schema = HeaterSchema()


class HeaterItemApi(ModelApi):
    """/api/heater/<id>."""

    model = Heater
    schema = HeaterSchema()


class HeaterStateApi(ModelApi):
    """/api/heater/<id>."""

    model = Heater
    schema = HeaterStateSchema()
