# -*- coding: utf-8 -*-
"""API views."""
from flask import Blueprint
from flask_restful import Api

from .heater import HeaterItemApi, HeaterListApi, HeaterStateApi
from .kettle import KettleApi, KettleItemApi
from .tempsensor import TempSensorItemApi, TempSensorListApi, TempSensorTempApi
from .pump import PumpItemApi, PumpListApi, PumpStateApi

blueprint = Blueprint("api", __name__, url_prefix="/api")
api = Api(blueprint)

api.add_resource(KettleApi, "/kettle")
api.add_resource(KettleItemApi, "/kettle/<id>")
api.add_resource(HeaterListApi, "/heater")
api.add_resource(HeaterItemApi, "/heater/<id>")
api.add_resource(HeaterStateApi, "/heater/<id>/state")
api.add_resource(TempSensorListApi, "/tempsensor")
api.add_resource(TempSensorItemApi, "/tempsensor/<id>")
api.add_resource(TempSensorTempApi, "/tempsensor/<id>/temperature")
api.add_resource(PumpListApi, "/pump")
api.add_resource(PumpItemApi, "/pump/<id>")
api.add_resource(PumpStateApi, "/pump/<id>/state")
