"""Heater views."""
from flask import current_app, request
from flask_restx import Namespace, Resource, fields

from ..models import Heater
from ..schemas import HeaterSchema, HeaterStateSchema

api = Namespace("Heater", description="Heater related operations")

nsmodel = api.model(
    "Heater",
    {
        "id": fields.Integer(readonly=True, description="Heater Identifier"),
        "name": fields.String(required=True, description="Heater Name"),
        "gpio_num": fields.Integer(required=True, description="Heater GPIO Number"),
        "state": fields.Boolean(
            default=False, description="True = Heater On, False = Heater Off"
        ),
        "active_low": fields.Boolean(
            default=False, description="Heater State logic is reversed"
        ),
        "kettle_id": fields.Integer(
            default=None,
            description="ID of the Kettle where the Heater is located.",
            nullable=True,
        ),
    },
)

nsmodelstat = api.model(
    "HeaterState",
    {
        "state": fields.Boolean(
            default=False, description="True = Heater On, False = Heater Off"
        ),
    },
)


@api.route("/")
class HeaterList(Resource):
    """Shows a list of all Heaters, and lets you POST to add new heaters."""

    @api.doc("list_heaters")
    @api.marshal_list_with(nsmodel)
    def get(self):
        """List all Heaters."""
        schema = HeaterSchema(many=True)
        query = Heater.query.all()
        return schema.dump(query)

    @api.doc("create_heater")
    @api.expect(nsmodel)
    def post(self):
        """Create a new Heater."""
        schema = HeaterSchema()
        # print(api.payload)
        # return Heater.create(**api.payload), 201
        data = schema.load(request.get_json())
        if not schema.validate(data):
            current_app.logger.info(f"New Item Data: {data}")
            new_item = Heater.create(**data)
            return schema.jsonify(new_item)
        return api.abort(404, message="Invalid Fields. Cannot Create Item")


@api.route("/<id>")
@api.param("id", "The Heater identifier")
@api.response(404, "Heater not found")
class HeaterItem(Resource):
    """Retrieve a heater instance."""

    @api.doc("get_heater")
    @api.marshal_with(nsmodel)
    def get(self, id):
        """Fetch a Heater given its identifier."""

        schema = HeaterSchema()
        query = Heater.get_by_id(id)
        if not query:
            api.abort(404, message="Heater {} doesn't exist".format(id))
        return schema.dump(query)

    @api.doc("delete_heater")
    @api.response(204, "Heater deleted")
    @api.response(404, "Heater does not exist")
    def delete(self, id):
        """Delete a heater given its identifier."""
        heater = Heater.get_by_id(id)
        if not heater:
            api.abort(404, message=f"Heater {id} doesn't exist")
        heater.delete()
        return "", 204

    @api.expect(nsmodel)
    @api.marshal_with(nsmodel)
    def put(self, id):
        """Update a heater given its identifier."""
        schema = HeaterSchema()
        heater = Heater.get_by_id(id)
        if not heater:
            api.abort(404, message=f"Heater {id} doesn't exist")

        data = schema.load(request.get_json(), partial=True)
        if data:
            for key, value in data.items():
                if value is not None:
                    if hasattr(heater, key):
                        setattr(heater, key, value)
            heater.update()
            return schema.dump(heater)
        return api.abort(404, message="Invalid Fields. Cannot Update heater")

@api.route("/<id>/state")
@api.param("id", "The Heater identifier")
@api.response(404, "Heater not found")
class HeaterItemState(Resource):
    """Retrieve a heater instance."""

    @api.doc("get_heater_state")
    @api.doc(model=nsmodelstat)
    @api.marshal_with(nsmodelstat)
    def get(self, id):
        """Fetch the current heater state."""

        schema = HeaterStateSchema()
        query = Heater.get_by_id(id)
        if not query:
            api.abort(404, message="Heater {} doesn't exist".format(id))
        return schema.dump({"state": query.current_state})

    @api.doc(model=nsmodelstat, body=nsmodelstat)
    @api.expect(nsmodelstat)
    def put(self, id):
        """Update the heater state."""
        schema = HeaterStateSchema()
        query = Heater.get_by_id(id)
        if not query:
            api.abort(404, message="Heater {} doesn't exist".format(id))
        data = schema.load(request.get_json())
        if data.get("state") is True:
            query.turn_on()
            return schema.dump(query)
        if data.get("state") is False:
            query.turn_off()
            return schema.dump(query)
        return api.abort(404, message="Invalid Fields. Cannot Update Item")
