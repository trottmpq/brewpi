# -*- coding: utf-8 -*-
"""TempSensor API views."""
from flask_restful import fields

from brewpi.temp_sensor.models import TempSensor

from .baseapi import BaseApi, BaseItemApi


class TempSensorApi(BaseApi):
    """View for '/api/tempsensor' ."""

    def __init__(self):
        """Define model and fields."""
        super(TempSensorApi, self).__init__()
        self.fields = {
            "name": fields.String,
            "gpio_num": fields.Integer,
        }
        self.model = TempSensor
        self.reqparse.add_argument("name", type=str)
        self.reqparse.add_argument("gpio_num", type=int)


class TempSensorItemApi(BaseItemApi):
    """/api/tempsensor/<id>."""

    def __init__(self):
        """Define model and fields."""
        super(TempSensorItemApi, self).__init__()
        self.fields = {
            "name": fields.String,
            "gpio_num": fields.Integer,
        }
        self.model = TempSensor
        self.reqparse.add_argument("name", type=str)
        self.reqparse.add_argument("gpio_num", type=int)
