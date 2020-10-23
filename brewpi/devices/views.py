# -*- coding: utf-8 -*-
"""Heater views."""
from flask import Blueprint
from flask_restx import Api, Namespace, Resource, fields
from sqlalchemy.sql.elements import Null

from .models import Heater

blueprint = Blueprint("devices", __name__, url_prefix="/devices")

api = Api(blueprint, title="Devices", version="1.0", description="A description")

HeaterNS = Namespace("Heater", description="Heater related operations")

heaterswaggermodel = api.model(
    "Heater",
    {
        "gpio_num": fields.Integer(required=True, description="The cat name"),
        "kettle_id": fields.Integer(default=None, nullable=True),
        "name": fields.String(required=True, description="The cat name"),
        "state": fields.Boolean(default=False),
        "id": fields.Integer(readonly=True, description="The Heater identifier"),
        "active_low": fields.Boolean(default=False),
    },
)


@HeaterNS.route("/")
class HeaterList(Resource):
    """Shows a list of all Heaters, and lets you POST to add new heaters"""

    @HeaterNS.doc("list_heaters")
    @HeaterNS.marshal_list_with(heaterswaggermodel)
    def get(self):
        """List all tasks"""
        return Heater.query.all()

    @HeaterNS.doc("create_heater")
    @HeaterNS.expect(heaterswaggermodel)
    @HeaterNS.marshal_with(heaterswaggermodel, code=201)
    def post(self):
        """Create a new Heater"""
        print(api.payload)
        return Heater.create(**api.payload), 201


api.add_namespace(HeaterNS)
