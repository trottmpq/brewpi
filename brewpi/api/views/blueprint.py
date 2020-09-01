# -*- coding: utf-8 -*-
"""API views."""
from flask import Blueprint
from flask_restful import Api

from .heater import HeaterApi, HeaterItemApi
from .kettle import KettleApi, KettleItemApi
from .tempsensor import TempSensorApi, TempSensorItemApi

blueprint = Blueprint("api", __name__, url_prefix="/api")
api = Api(blueprint)

api.add_resource(KettleApi, "/kettle")
api.add_resource(KettleItemApi, "/kettle/<id>")
api.add_resource(HeaterApi, "/heater")
api.add_resource(HeaterItemApi, "/heater/<id>")
api.add_resource(TempSensorApi, "/tempsensor")
api.add_resource(TempSensorItemApi, "/tempsensor/<id>")
