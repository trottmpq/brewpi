# -*- coding: utf-8 -*-
"""Kettle API views."""

from brewpi.devices.models import Kettle
from brewpi.devices.schemas import KettleSchema

from .baseapi import ListApi, ModelApi


class KettleApi(ListApi):
    """View for '/api/kettle' ."""

    model = Kettle
    schema = KettleSchema()


class KettleItemApi(ModelApi):
    """/api/kettle/<id>."""

    model = Kettle
    schema = KettleSchema()
