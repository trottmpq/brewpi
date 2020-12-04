# -*- coding: utf-8 -*-
"""API views."""
from flask import Blueprint
from flask_restx import Api

from .views import heater, kettle, pump, temp_sensor

blueprint = Blueprint("devices", __name__)

api = Api(
    blueprint,
    title="Devices",
    version="1.0",
    description="Api to control all the various devices in the brewery",
)

api.add_namespace(heater.api)
api.add_namespace(kettle.api)
api.add_namespace(pump.api)
api.add_namespace(temp_sensor.api)
