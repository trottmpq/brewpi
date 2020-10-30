"""TempSensor views."""
from flask import current_app, request
from flask_restx import Namespace, Resource, fields

from ..models import TempSensor
from ..schemas import TempSensorSchema, TempSensorTempSchema

api = Namespace("TempSensor", description="TempSensor related operations")

nsmodel = api.model(
    "TempSensor",
    {
        "id": fields.Integer(readonly=True, description="TempSensor Identifier"),
        "name": fields.String(required=True, description="TempSensor Name"),
        "gpio_num": fields.Integer(required=True, description="TempSensor GPIO Number"),
        "temperature": fields.Float(
            default=False, description="Temperature in degrees Celcius"
        ),
        "active_low": fields.Boolean(
            default=False, description="TempSensor State logic is reversed"
        ),
        "kettle_id": fields.Integer(
            default=None,
            description="ID of the Kettle where the TempSensor is located.",
            nullable=True,
        ),
    },
)

nsmodelstat = api.model(
    "TempSensorTemperature",
    {
        "temperature": fields.Float(
            default=False, description="Temperature in degrees Celcius"
        ),
    },
)


@api.route("/")
class TempSensorList(Resource):
    """Shows a list of all TempSensors, and lets you POST to add new temp_sensors."""

    @api.doc("list_temp_sensors")
    @api.marshal_list_with(nsmodel)
    def get(self):
        """List all TempSensors."""
        schema = TempSensorSchema(many=True)
        query = TempSensor.query.all()
        if query:
            for i in query:
                i.current_temperature

        return schema.dump(query)

    @api.doc("create_temp_sensor")
    @api.expect(nsmodel)
    def post(self):
        """Create a new TempSensor."""
        schema = TempSensorSchema()
        data = schema.load(request.get_json())
        if not schema.validate(data):
            current_app.logger.info(f"New Item Data: {data}")
            new_item = TempSensor.create(**data)
            return schema.jsonify(new_item)
        return api.abort(404, message="Invalid Fields. Cannot Create Item")


@api.route("/<id>")
@api.param("id", "The TempSensor identifier")
@api.response(404, "TempSensor not found")
class TempSensorItem(Resource):
    """Retrieve a temp_sensor instance."""

    @api.doc("get_temp_sensor")
    @api.marshal_with(nsmodel)
    @api.response(404, "Temp Sensor does not exist")
    def get(self, id):
        """Fetch a TempSensor given its identifier."""

        schema = TempSensorSchema()
        query = TempSensor.get_by_id(id)
        if not query:
            api.abort(404, message=f"TempSensor {id} doesn't exist")
        query.current_temperature
        return schema.dump(query)

    @api.doc("delete_tempsensor")
    @api.response(204, "Temp Sensor deleted")
    @api.response(404, "Temp Sensor does not exist")
    def delete(self, id):
        """Delete a tempsensor given its identifier."""
        tempsense = TempSensor.get_by_id(id)
        if not tempsense:
            api.abort(404, message=f"TempSensor {id} doesn't exist")
        tempsense.delete()
        return "", 204

    @api.expect(nsmodel)
    @api.marshal_with(nsmodel)
    def put(self, id):
        """Update a tempsensor given its identifier."""
        schema = TempSensorSchema()
        tempsense = TempSensor.get_by_id(id)
        if not tempsense:
            api.abort(404, message=f"TempSensor {id} doesn't exist")

        data = schema.load(request.get_json(), partial=True)
        if data:
            for k, v in data.items():
                if v is not None:
                    if hasattr(tempsense, k):
                        setattr(tempsense, k, v)
            tempsense.update()
            return schema.dump(tempsense)
        return api.abort(404, message="Invalid Fields. Cannot Update tempsensor")


@api.route("/<id>/temperature")
@api.param("id", "The TempSensor identifier")
@api.response(404, "TempSensor not found")
class TempSensorItemState(Resource):
    """Retrieve a temp_sensor instance."""

    @api.doc("get_temp_sensor_temperature")
    @api.doc(model=nsmodelstat)
    @api.marshal_with(nsmodelstat)
    def get(self, id):
        """Fetch the current temp_sensor state."""

        schema = TempSensorTempSchema()
        query = TempSensor.get_by_id(id)
        if not query:
            api.abort(404, message=f"TempSensor {id} doesn't exist")
        current_app.logger.info(
            f"{query.name} on gpio {query.gpio_num} reads {query.current_temperature:.2f}C"
        )
        return schema.dump({"temperature": query.current_temperature})
