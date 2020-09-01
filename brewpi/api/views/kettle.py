# -*- coding: utf-8 -*-
"""Kettle API views."""
from flask_restful import fields

from brewpi.kettle.models import Kettle

from .baseapi import BaseApi, BaseItemApi


class KettleApi(BaseApi):
    """View for '/api/kettle' ."""

    def __init__(self):
        """Define model and fields."""
        super(KettleApi, self).__init__()
        self.fields = {
            "name": fields.String,
            "heater_id": fields.Integer,
            "tempsense_id": fields.Integer,
        }
        self.model = Kettle
        self.reqparse.add_argument("name", type=str)
        self.reqparse.add_argument("heater_id", type=int)
        self.reqparse.add_argument("tempsense_id", type=int)


class KettleItemApi(BaseItemApi):
    """/api/kettle/<id>."""

    def __init__(self):
        """Define model and fields."""
        super(KettleItemApi, self).__init__()
        self.fields = {
            "name": fields.String,
            "heater_id": fields.Integer,
            "tempsense_id": fields.Integer,
        }
        self.model = Kettle
        self.reqparse.add_argument("name", type=str)
        self.reqparse.add_argument("heater_id", type=int)
        self.reqparse.add_argument("tempsense_id", type=int)
