"""Kettle views."""
from flask import current_app, request
from flask_restx import Namespace, Resource, fields

from ..models import Kettle
from ..schemas import KettleSchema
from .heater import nsmodel as heatermodel
from .pump import nsmodel as pumpmodel
from .temp_sensor import nsmodel as tempsensormodel

api = Namespace("Kettle", description="Kettle related operations")

nsmodel = api.model(
    "Kettle",
    {
        "id": fields.Integer(readonly=True, description="Kettle Identifier"),
        "name": fields.String(required=True, description="Kettle Name"),
        "target_temp": fields.Float(
            default=0.0, description="Kettle target temperature"
        ),
        "temp_sensor": fields.Nested(tempsensormodel, allow_null=True),
        "pump": fields.Nested(pumpmodel, allow_null=True),
        "heater": fields.Nested(heatermodel, allow_null=True),
    },
)

nsmodeltemp = api.model(
    "KettleTemperature",
    {
        "temperature": fields.Float(
            default=0.0, description="Temperature in degrees Celcius"
        ),
    },
)

nsmodelheaterstate = api.model(
    "KettleHeaterState",
    {
        "state": fields.Boolean(
            default=False, description="True = Heater On, False = Heater Off"
        ),
    },
)

nsmodelpumpstate = api.model(
    "KettlePumpState",
    {
        "state": fields.Boolean(
            default=False, description="True = Pump On, False = Pump Off"
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
        for kettle in query:
            if kettle.temp_sensor:
                kettle.temp_sensor.current_temperature
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


@api.route("/<id>")
@api.param("id", "The Kettle identifier")
@api.response(404, "Kettle not found")
class KettleItem(Resource):
    """Retrieve a kettle instance."""

    @api.doc("get_kettle")
    @api.marshal_with(nsmodel)
    def get(self, id):
        """Fetch a Kettle given its identifier."""

        schema = KettleSchema()
        query = Kettle.get_by_id(id)
        if not query:
            api.abort(404, message="Kettle {} doesn't exist".format(id))
        if query.temp_sensor:
            query.temp_sensor.current_temperature
        return schema.dump(query)

    @api.doc("delete_kettle")
    @api.response(204, "Kettle deleted")
    @api.response(404, "Kettle does not exist")
    def delete(self, id):
        """Delete a kettle given its identifier."""
        kettle = Kettle.get_by_id(id)
        if not kettle:
            api.abort(404, message=f"Kettle {id} doesn't exist")
        kettle.delete()
        return "", 204

    @api.expect(nsmodel)
    @api.marshal_with(nsmodel)
    def put(self, id):
        """Update a kettle given its identifier."""
        schema = KettleSchema()
        kettle = Kettle.get_by_id(id)
        if not kettle:
            api.abort(404, message=f"Kettle {id} doesn't exist")

        data = schema.load(request.get_json(), partial=True)
        if data:
            for key, value in data.items():
                if value is not None:
                    if hasattr(kettle, key):
                        setattr(kettle, key, value)
            kettle.update()
            return schema.dump(kettle)
        return api.abort(404, message="Invalid Fields. Cannot Update kettle")


@api.route("/<id>/temperature")
@api.param("id", "The kettle identifier")
@api.response(404, "kettle tempsensor not found")
class KettleItemTemperature(Resource):
    """Retrieve a temp_sensor instance."""

    @api.doc("get_kettle_temperature")
    @api.doc(model=nsmodeltemp)
    @api.marshal_with(nsmodeltemp)
    def get(self, id):
        """Fetch the current temp_sensor state."""

        # schema = KettleSchema()
        query = Kettle.get_by_id(id)
        if not query:
            api.abort(404, message=f"kettle {id} doesn't exist")
        if not query.temp_sensor:
            api.abort(
                404, message=f"kettle {id} doesn't have a temp sensor configured."
            )

        temperature = query.temp_sensor.current_temperature
        current_app.logger.info(
            f"{query.name}, {query.temp_sensor.name} on gpio {query.temp_sensor.gpio_num} reads {temperature:.2f}C"
        )
        return {"temperature": temperature}


@api.route("/<id>/heaterstate")
@api.param("id", "The kettle identifier")
@api.response(404, "kettle heater not found")
class KettleItemHeaterState(Resource):
    """Retrieve a heater instance from the kettle."""

    @api.doc("get_kettle_heater")
    @api.doc(model=nsmodelheaterstate)
    @api.marshal_with(nsmodelheaterstate)
    def get(self, id):
        """Fetch the current heater state."""

        # schema = KettleSchema()
        query = Kettle.get_by_id(id)
        if not query:
            api.abort(404, message=f"kettle {id} doesn't exist")
        if not query.heater:
            api.abort(404, message=f"kettle {id} doesn't have a heater configured.")

        current_state = query.heater.current_state
        current_app.logger.info(
            f"{query.name}, {query.heater.name} on gpio {query.heater.gpio_num} reads {current_state}"
        )
        return {"state": current_state}


@api.route("/<id>/pumpstate")
@api.param("id", "The kettle identifier")
@api.response(404, "kettle pump not found")
class KettleItemPumpState(Resource):
    """Retrieve a pump instance from the kettle."""

    @api.doc("get_kettle_pump")
    @api.doc(model=nsmodelpumpstate)
    @api.marshal_with(nsmodelpumpstate)
    def get(self, id):
        """Fetch the current pump state."""

        # schema = KettleSchema()
        query = Kettle.get_by_id(id)
        if not query:
            api.abort(404, message=f"kettle {id} doesn't exist")
        if not query.pump:
            api.abort(404, message=f"kettle {id} doesn't have a pump configured.")

        current_state = query.pump.current_state
        current_app.logger.info(
            f"{query.name}, {query.pump.name} on gpio {query.pump.gpio_num} reads {current_state}"
        )
        return {"state": current_state}
