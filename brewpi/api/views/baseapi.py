# -*- coding: utf-8 -*-
"""Heater API views."""
from flask import current_app, request
from flask_restful import Resource, abort


class BaseApi(Resource):
    """View for '/api/heater' ."""

    def get(self):
        """Return the entire inventory collection."""
        results = self.model.query.all()
        self.schema.many = True
        response = self.schema.dump(results)
        self.schema.many = False
        return response

    def post(self):
        """Create an item."""
        args = request.get_json()
        data = self.schema.load(args)
        current_app.logger.info(f"New Item Data: {data}")
        new_item = self.model.create(**data)
        return self.schema.jsonify(new_item)


class BaseItemApi(Resource):
    """/api/heater/<id>."""

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
        return self.schema.dump(item)

    def put(self, id):
        """Update/replace an item."""
        item = self.abort_if_item_doesnt_exist(id)
        args = request.get_json()
        data = self.schema.validate(args, partial=True)
        if not data:
            for k, v in args.items():
                if v is not None:
                    if hasattr(item, k):
                        setattr(item, k, v)
            item.save()
            return self.schema.dump(item)
        return abort(404, message='Invalid Fields. Cannot Update Item')

    def delete(self, id):
        """Delete an item."""
        item = self.abort_if_item_doesnt_exist(id)
        item.delete()
        return self.schema.dump(item)
