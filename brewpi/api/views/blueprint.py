# -*- coding: utf-8 -*-
"""API views."""
from flask import Blueprint

from .heater import HeaterApi, HeaterItemApi
from .tempsensor import TempSensorApi, TempSensorItemApi

blueprint = Blueprint("api", __name__, url_prefix="/api", static_folder="../static")

blueprint.add_url_rule("/heater", view_func=HeaterApi.as_view("heater_api"))
blueprint.add_url_rule(
    "/heater/<id>", view_func=HeaterItemApi.as_view("heater_item_api")
)
blueprint.add_url_rule("/tempsensor", view_func=TempSensorApi.as_view("tempsensor_api"))
blueprint.add_url_rule(
    "/tempsensor/<id>", view_func=TempSensorItemApi.as_view("tempsensor_item_api")
)
