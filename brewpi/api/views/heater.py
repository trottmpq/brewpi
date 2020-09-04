# -*- coding: utf-8 -*-
"""Heater API views."""

from brewpi.devices.models import Heater
from brewpi.devices.schemas import HeaterSchema

from .baseapi import BaseApi, BaseItemApi


class HeaterApi(BaseApi):
    """View for '/api/heater' ."""

    model = Heater
    schema = HeaterSchema()


class HeaterItemApi(BaseItemApi):
    """/api/heater/<id>."""

    model = Heater
    schema = HeaterSchema()
