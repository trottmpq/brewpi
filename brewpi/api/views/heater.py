# -*- coding: utf-8 -*-
"""Heater API views."""
from flask_restful import fields

from brewpi.heater.models import Heater

from .baseapi import BaseApi, BaseItemApi


class HeaterApi(BaseApi):
    """View for '/api/heater' ."""

    def __init__(self):
        """Define model and fields."""
        super(HeaterApi, self).__init__()
        self.fields = {
            "name": fields.String,
            "gpio_num": fields.Integer,
        }
        self.model = Heater
        self.reqparse.add_argument("name", type=str)
        self.reqparse.add_argument("gpio_num", type=int)


class HeaterItemApi(BaseItemApi):
    """/api/heater/<id>."""

    def __init__(self):
        """Define model and fields."""
        super(HeaterItemApi, self).__init__()
        self.fields = {
            "name": fields.String,
            "gpio_num": fields.Integer,
        }
        self.model = Heater
        self.reqparse.add_argument("name", type=str)
        self.reqparse.add_argument("gpio_num", type=int)
