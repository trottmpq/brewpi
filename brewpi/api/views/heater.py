# -*- coding: utf-8 -*-
"""Heater API views."""
from flask import jsonify, make_response, request
from flask.views import MethodView

from brewpi.heater.models import Heater


class HeaterApi(MethodView):
    """View for '/api/heater' ."""

    def get(self):
        """Return the entire inventory collection."""
        heaters = Heater.query.all()
        heaters_array = [heater.serialize() for heater in heaters]
        return make_response(jsonify(heaters_array), 200)


class HeaterItemApi(MethodView):
    """/api/heater/<id>."""

    error = {
        "heaterNotFound": {
            "errorCode": "heaterNotFound",
            "errorMessage": "Heater not found",
        },
        "heaterAlreadyExists": {
            "errorCode": "heaterAlreadyExists",
            "errorMessage": "Could not create Heater. Heater already exists",
        },
    }

    def get(self, id):
        """Get an item."""
        heater = Heater.get_by_id(id)
        if not heater:
            return make_response(jsonify(self.error["heaterNotFound"]), 400)

        return make_response(jsonify(heater.serialize()), 200)

    def post(self, id):
        """Create an item."""
        heater = Heater.get_by_id(id)
        if heater:
            return make_response(jsonify(self.error["heaterAlreadyExists"]), 400)

        new_heater = Heater.create(
            name=request.json.get("name", None),
            gpio_num=request.json.get("gpio_num", None),
        )
        return make_response(jsonify(new_heater.serialize()))

    def put(self, id):
        """Update/replace an item."""
        heater = Heater.get_by_id(id)
        if not heater:
            return make_response(jsonify(self.error["heaterNotFound"]), 400)

        heater.name = request.json.get("name", heater.name)
        heater.heater = request.json.get("gpio_num", heater.gpio_num)
        heater.state = request.json.get("state", heater.state)

        heater.save()
        return make_response(jsonify(heater.serialize()))

    def delete(self, id):
        """Delete an item."""
        heater = Heater.get_by_id(id)
        if not heater:
            return make_response(jsonify(self.error["heaterNotFound"]), 400)

        heater.delete()
        return make_response(jsonify({}), 200)
