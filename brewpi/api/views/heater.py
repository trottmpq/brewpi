# -*- coding: utf-8 -*-
"""Heater API views."""
from flask import jsonify, make_response, request

from brewpi.heater.models import Heater

from .baseapi import BaseApi, BaseItemApi


class HeaterApi(BaseApi):
    """View for '/api/heater' ."""

    model = Heater


class HeaterItemApi(BaseItemApi):
    """/api/heater/<id>."""

    model = Heater

    def post(self, id):
        """Create an item."""
        heater = self.model.get_by_id(id)
        if heater:
            return make_response(jsonify(self.error["heaterAlreadyExists"]), 400)

        new_heater = self.model.create(
            name=request.json.get("name", None),
            gpio_num=request.json.get("gpio_num", None),
        )
        return make_response(jsonify(new_heater.serialize()))

    def put(self, id):
        """Update/replace an item."""
        heater = self.model.get_by_id(id)
        if not heater:
            return make_response(jsonify(self.error["heaterNotFound"]), 400)

        heater.name = request.json.get("name", heater.name)
        heater.gpio_num = request.json.get("gpio_num", heater.gpio_num)
        heater.state = request.json.get("state", heater.state)

        heater.save()
        return make_response(jsonify(heater.serialize()))
