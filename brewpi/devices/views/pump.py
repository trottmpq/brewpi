"""Pump views."""
from flask import current_app, request
from flask_restx import Namespace, Resource, fields

from ..models import Pump
from ..schemas import PumpSchema, PumpStateSchema

api = Namespace("Pump", description="Pump related operations")

nsmodel = api.model(
    "Pump",
    {
        "id": fields.Integer(readonly=True, description="Pump Identifier"),
        "name": fields.String(required=True, description="Pump Name"),
        "gpio_num": fields.Integer(required=True, description="Pump GPIO Number"),
        "state": fields.Boolean(
            default=False, description="True = Pump On, False = Pump Off"
        ),
        "active_low": fields.Boolean(
            default=False, description="Pump State logic is reversed"
        ),
        "kettle_id": fields.Integer(
            default=None,
            description="ID of the Kettle where the Pump is located.",
            nullable=True,
        ),
    },
)

nsmodelstat = api.model(
    "PumpState",
    {
        "state": fields.Boolean(
            default=False, description="True = Pump On, False = Pump Off"
        ),
    },
)


@api.route("/")
class PumpList(Resource):
    """Shows a list of all Pumps, and lets you POST to add new pumps."""

    @api.doc("list_pumps")
    @api.marshal_list_with(nsmodel)
    def get(self):
        """List all Pumps."""
        schema = PumpSchema(many=True)
        query = Pump.query.all()
        return schema.dump(query)

    @api.doc("create_pump")
    @api.expect(nsmodel)
    def post(self):
        """Create a new Pump."""
        schema = PumpSchema()
        data = schema.load(request.get_json())
        if not schema.validate(data):
            current_app.logger.info(f"New Item Data: {data}")
            new_item = Pump.create(**data)
            return schema.jsonify(new_item)
        return api.abort(404, message="Invalid Fields. Cannot Create Item")


@api.route("/<id>")
@api.param("id", "The Pump identifier")
@api.response(404, "Pump not found")
class PumpItem(Resource):
    """Retrieve a pump instance."""

    @api.doc("get_pump")
    @api.marshal_with(nsmodel)
    def get(self, id):
        """Fetch a Pump given its identifier."""

        schema = PumpSchema()
        query = Pump.get_by_id(id)
        if not query:
            api.abort(404, message="Pump {} doesn't exist".format(id))
        return schema.dump(query)
    
    @api.doc("delete_pump")
    @api.response(204, "Pump deleted")
    @api.response(404, "Pump does not exist")
    def delete(self, id):
        """Delete a tempsensor given its identifier."""
        pump = Pump.get_by_id(id)
        if not pump:
            api.abort(404, message=f"Pump {id} doesn't exist")
        pump.delete()
        return "", 204

    @api.expect(nsmodel)
    @api.marshal_with(nsmodel)
    def put(self, id):
        """Update a pump given its identifier."""
        schema = PumpSchema()
        pump = Pump.get_by_id(id)
        if not pump:
            api.abort(404, message=f"Pump {id} doesn't exist")

        data = schema.load(request.get_json(), partial=True)
        if data:
            for key, value in data.items():
                if value is not None:
                    if hasattr(pump, key):
                        setattr(pump, key, value)
            pump.update()
            return schema.dump(pump)
        return api.abort(404, message="Invalid Fields. Cannot Update pump")


@api.route("/<id>/state")
@api.param("id", "The Pump identifier")
@api.response(404, "Pump not found")
class PumpItemState(Resource):
    """Retrieve a pump instance."""

    @api.doc("get_pump_state")
    @api.doc(model=nsmodelstat)
    @api.marshal_with(nsmodelstat)
    def get(self, id):
        """Fetch the current pump state."""

        schema = PumpStateSchema()
        query = Pump.get_by_id(id)
        if not query:
            api.abort(404, message="Pump {} doesn't exist".format(id))
        return schema.dump({"state": query.current_state})

    @api.doc(model=nsmodelstat, body=nsmodelstat)
    @api.expect(nsmodelstat)
    def put(self, id):
        """Update the pump state."""
        schema = PumpStateSchema()
        query = Pump.get_by_id(id)
        if not query:
            api.abort(404, message="Pump {} doesn't exist".format(id))
        data = schema.load(request.get_json())
        if data.get("state") is True:
            query.turn_on()
            return schema.dump(query)
        if data.get("state") is False:
            query.turn_off()
            return schema.dump(query)
        return api.abort(404, message="Invalid Fields. Cannot Update Item")
