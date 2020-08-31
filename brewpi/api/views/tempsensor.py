# -*- coding: utf-8 -*-
"""Heater API views."""
from flask import jsonify, make_response, request

from brewpi.temp_sensor.models import TempSensor

from .baseapi import BaseApi, BaseItemApi


class TempSensorApi(BaseApi):
    """View for '/api/heater' ."""

    model = TempSensor


class TempSensorItemApi(BaseItemApi):
    """/api/heater/<id>."""

    model = TempSensor

    def post(self, id):
        """Create an item."""
        tempsensor = self.model.get_by_id(id)
        if tempsensor:
            return make_response(jsonify(self.error["heaterAlreadyExists"]), 400)

        new_tempsensor = self.model.create(
            name=request.json.get("name", None),
            gpio_num=request.json.get("gpio_num", None),
        )
        return make_response(jsonify(new_tempsensor.serialize()))

    def put(self, id):
        """Update/replace an item."""
        tempsensor = self.model.get_by_id(id)
        if not tempsensor:
            return make_response(jsonify(self.error["heaterNotFound"]), 400)

        tempsensor.name = request.json.get("name", tempsensor.name)
        tempsensor.gpio_num = request.json.get("gpio_num", tempsensor.gpio_num)
        tempsensor.temperature = request.json.get("temperature", tempsensor.temperature)

        tempsensor.save()
        return make_response(jsonify(tempsensor.serialize()))
