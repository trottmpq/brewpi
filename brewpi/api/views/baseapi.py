# -*- coding: utf-8 -*-
"""Heater API views."""
from flask import jsonify, make_response, request
from flask.views import MethodView


class BaseApi(MethodView):
    """View for '/api/heater' ."""

    __abstract__ = True
    model = None

    def get(self):
        """Return the entire inventory collection."""
        results = self.model.query.all()
        results_array = [result.serialize() for result in results]
        return make_response(jsonify(results_array), 200)


class BaseItemApi(MethodView):
    """/api/heater/<id>."""

    __abstract__ = True
    model = None
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
        item = self.model.get_by_id(id)
        if not item:
            return make_response(jsonify(self.error["heaterNotFound"]), 400)

        return make_response(jsonify(item.serialize()), 200)

    def post(self, id):
        """Create an item."""
        item = self.model.get_by_id(id)
        if item:
            return make_response(jsonify(self.error["heaterAlreadyExists"]), 400)

        new_item = self.model.create(
            name=request.json.get("name", None),
            gpio_num=request.json.get("gpio_num", None),
        )
        return make_response(jsonify(new_item.serialize()))

    def put(self, id):
        """Update/replace an item."""
        item = self.model.get_by_id(id)
        if not item:
            return make_response(jsonify(self.error["heaterNotFound"]), 400)

        # TODO: automatic create this
        item.name = request.json.get("name", item.name)
        item.heater = request.json.get("gpio_num", item.gpio_num)
        item.state = request.json.get("state", item.state)

        item.save()
        return make_response(jsonify(item.serialize()))

    def delete(self, id):
        """Delete an item."""
        item = self.model.get_by_id(id)
        if not item:
            return make_response(jsonify(self.error["heaterNotFound"]), 400)

        item.delete()
        return make_response(jsonify({}), 200)
