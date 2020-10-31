# -*- coding: utf-8 -*-
"""API views."""
from flask import Blueprint
from flask_restx import Api

from .heater import api as heaterns
from .kettle import api as kettlens
from .pump import api as pumpns
from .temp_sensor import api as tempsensorns

blueprint = Blueprint("devices", __name__, url_prefix="/devices")

api = Api(
    blueprint,
    title="Devices",
    version="1.0",
    description="Api to control all the various devices in the brewery",
)

api.add_namespace(heaterns)
api.add_namespace(pumpns)
api.add_namespace(tempsensorns)
api.add_namespace(kettlens)
