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

parser = api.parser()
parser.add_argument(
    "state", type=bool, required=True, help="The desired Heater state", location="form"
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
        schema = HeaterSchema(many=True)
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


@api.route("/<id>/state")
@api.param("id", "The Heater identifier")
@api.response(404, "Heater not found")
class HeaterItemState(Resource):
    """Retrieve a heater instance."""

    @api.doc("get_heater")
    @api.marshal_with(nsmodelstat)
    def get(self, id):
        """Fetch the current heater state."""

        schema = HeaterStateSchema()
        query = Heater.get_by_id(id)
        if not query:
            api.abort(404, message="Heater {} doesn't exist".format(id))
        return schema.dump(query)

    @api.doc(parser=parser)
    @api.expect(nsmodelstat)
    def put(self, id):
        """Update the heater state."""
        schema = HeaterStateSchema()
        query = Heater.get_by_id(id)
        if not query:
            api.abort(404, message="Heater {} doesn't exist".format(id))
        args = parser.parse_args()
        data = schema.validate(args)
        if not data:
            if args["state"] is True:
                query.turn_on()
                return schema.dump(query)
            if args["state"] is False:
                query.turn_off()
                return schema.dump(query)
        return api.abort(404, message="Invalid Fields. Cannot Update Item")
