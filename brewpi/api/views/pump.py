# -*- coding: utf-8 -*-
"""Pump API views."""

from brewpi.devices.models import Pump
from brewpi.devices.schemas import PumpSchema, PumpStateSchema

from .baseapi import ListApi, ModelApi, RetrieveUpdateApi


class PumpListApi(ListApi):
    """View for '/api/Pump' ."""

    model = Pump
    schema = PumpSchema()


class PumpItemApi(ModelApi):
    """/api/Pump/<id>."""

    model = Pump
    schema = PumpSchema()


class PumpStateApi(RetrieveUpdateApi):
    """/api/Pump/<id>."""

    model = Pump
    schema = PumpStateSchema()
