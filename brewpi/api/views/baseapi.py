# -*- coding: utf-8 -*-
"""Heater API views."""
from flask import current_app, jsonify, make_response
from flask_restful import Resource, abort, marshal, reqparse


class BaseApi(Resource):
    """View for '/api/heater' ."""

    def __init__(self):
        """Initialise the Base API Class."""
        self.fields = None
        self.model = None
        self.reqparse = reqparse.RequestParser()

    def get(self):
        """Return the entire inventory collection."""
        results = self.model.query.all()
        results_array = [result.serialize() for result in results]
        return jsonify(results_array)

    def post(self):
        """Create an item."""
        args = self.reqparse.parse_args()
        data = dict(marshal(args, self.fields))
        current_app.logger.info(f"New Item Data: {data}")
        new_item = self.model.create(**data)
        return new_item.serialize(), 201


class BaseItemApi(Resource):
    """/api/heater/<id>."""

    def __init__(self):
        """Initialise the Base API Class."""
        self.fields = None
        self.model = None
        self.reqparse = reqparse.RequestParser()

    def abort_if_item_doesnt_exist(self, id):
        """Return a 404 if item doesn't exist."""
        item = self.model.get_by_id(id)
        if not item:
            abort(404, message="Item {} doesn't exist".format(id))
        return item

    def abort_if_item_does_exist(self, id):
        """Return a 404 if item doesn't exist."""
        item = self.model.get_by_id(id)
        if item:
            abort(404, message="Item {} already exists".format(id))
        return item

    def get(self, id):
        """Get an item."""
        item = self.abort_if_item_doesnt_exist(id)
        return jsonify(item.serialize())

    def put(self, id):
        """Update/replace an item."""
        item = self.abort_if_item_doesnt_exist(id)
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                if hasattr(item, k):
                    setattr(item, k, v)
        item.save()
        return make_response(jsonify(item.serialize()))

    def delete(self, id):
        """Delete an item."""
        item = self.abort_if_item_doesnt_exist(id)
        item.delete()
        return jsonify({}), 204
