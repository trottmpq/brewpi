"""Kettle views."""
from flask import current_app, request
from flask_restx import Namespace, Resource, fields

from ..models import Kettle
from ..schemas import KettleSchema

api = Namespace("Kettle", description="Kettle related operations")

nsmodel = api.model(
    "Kettle",
    {
        "id": fields.Integer(readonly=True, description="Kettle Identifier"),
        "name": fields.String(required=True, description="Kettle Name"),
        "target_temp": fields.Float(
            default=0.0, description="Kettle target temperature"
        ),
    },
)


@api.route("/")
class KettleList(Resource):
    """Shows a list of all Kettles, and lets you POST to add new Kettles."""

    @api.doc("list_kettles")
    @api.marshal_list_with(nsmodel)
    def get(self):
        """List all Kettles."""
        schema = KettleSchema(many=True)
        query = Kettle.query.all()
        return schema.dump(query)

    @api.doc("create_kettle")
    @api.expect(nsmodel)
    def post(self):
        """Create a new Kettle."""
        schema = KettleSchema()
        # print(api.payload)
        # return Kettle.create(**api.payload), 201
        data = schema.load(request.get_json())
        if not schema.validate(data):
            current_app.logger.info(f"New Item Data: {data}")
            new_item = Kettle.create(**data)
            return schema.jsonify(new_item)
        return api.abort(404, message="Invalid Fields. Cannot Create Item")
