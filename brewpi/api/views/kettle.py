# -*- coding: utf-8 -*-
"""Kettle API views."""

from brewpi.devices.models import Kettle
from brewpi.devices.schemas import KettleSchema

from .baseapi import BaseApi, BaseItemApi


class KettleApi(BaseApi):
    """View for '/api/kettle' ."""

    model = Kettle
    schema = KettleSchema()


class KettleItemApi(BaseItemApi):
    """/api/kettle/<id>."""

    model = Kettle
    schema = KettleSchema()
