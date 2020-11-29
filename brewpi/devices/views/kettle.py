"""Kettle views."""
from flask import current_app, request
from flask_restx import Namespace, Resource, fields

from ..models import Kettle
from ..schemas import KettleSchema, KettleStateSchema, KettleTempSchema
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
        "is_running": fields.Boolean(required=True, description="Control loop running"),
        "hyst_window": fields.Float(
            default=0.0, description="Kettle temperature hysteresis"
        ),
        "temp_sensor": fields.Nested(tempsensormodel, allow_null=True),
        "pump": fields.Nested(pumpmodel, allow_null=True),
        "heater_id": fields.Integer(
            default=None, description="ID of the Heater", nullable=True,
        ),
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

nsmodelloopstate = api.model(
    "KettleLoopState",
    {"state": fields.Boolean(default=False, description="True = Loop running")},
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

    @api.expect(nsmodelheaterstate)
    @api.marshal_with(nsmodelheaterstate)
    def put(self, id):
        """Update a kettles heater given its identifier."""
        schema = KettleStateSchema()
        kettle = Kettle.get_by_id(id)
        if not kettle:
            api.abort(404, message=f"Kettle {id} doesn't exist")
        if not kettle.heater:
            api.abort(404, message=f"kettle {id} doesn't have a heater configured.")

        data = schema.load(request.get_json(), partial=True)
        if data:
            if data.get("state") is True:
                kettle.heater.turn_on()
            if data.get("state") is False:
                kettle.heater.turn_off()
            return schema.dump({"state": kettle.heater.current_state})
        current_app.logger.info(
            f"{kettle.name}, {kettle.heater.name} on gpio {kettle.heater.gpio_num} set to {kettle.heater.current_state}"
        )
        return api.abort(404, message="Invalid Fields. Cannot Update kettle")


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

    @api.expect(nsmodelpumpstate)
    @api.marshal_with(nsmodelpumpstate)
    def put(self, id):
        """Update a kettles pump given its identifier."""
        schema = KettleStateSchema()
        kettle = Kettle.get_by_id(id)
        if not kettle:
            api.abort(404, message=f"Kettle {id} doesn't exist")
        if not kettle.pump:
            api.abort(404, message=f"kettle {id} doesn't have a pump configured.")

        data = schema.load(request.get_json(), partial=True)
        if data:
            if data.get("state") is True:
                kettle.pump.turn_on()
            if data.get("state") is False:
                kettle.pump.turn_off()
            return schema.dump({"state": kettle.pump.current_state})
        current_app.logger.info(
            f"{kettle.name}, {kettle.pump.name} on gpio {kettle.pump.gpio_num} set to {kettle.pump.current_state}"
        )
        return api.abort(404, message="Invalid Fields. Cannot Update kettle")


@api.route("/<id>/targettemp")
@api.param("id", "The kettle identifier")
@api.response(404, "kettle not found")
class KettleItemTargetTemp(Resource):
    """Retrieve the target temp from the kettle."""

    @api.doc("get_kettle_target_temp")
    @api.doc(model=nsmodeltemp)
    @api.marshal_with(nsmodeltemp)
    def get(self, id):
        """Fetch the current target temp."""

        query = Kettle.get_by_id(id)
        if not query:
            api.abort(404, message=f"kettle {id} doesn't exist")

        current_app.logger.info(
            f"{query.name}'s target temp is {query.current_target_temperature}C"
        )
        return {"temperature": query.current_target_temperature}

    @api.expect(nsmodeltemp)
    @api.marshal_with(nsmodeltemp)
    def put(self, id):
        """Update a kettles target temperature given its identifier."""
        schema = KettleTempSchema()
        kettle = Kettle.get_by_id(id)
        if not kettle:
            api.abort(404, message=f"Kettle {id} doesn't exist")

        data = schema.load(request.get_json(), partial=True)
        if data:
            if data.get("temperature"):
                kettle.current_target_temperature = data.get("temperature")
            current_app.logger.info(
                f"{kettle.name}'s target temp is {kettle.current_target_temperature}C"
            )
            return schema.dump({"temperature": kettle.current_target_temperature})
        return api.abort(404, message="Invalid Fields. Cannot Update kettle")


@api.route("/<id>/controlloop")
@api.param("id", "The kettle identifier")
@api.response(404, "kettle not found")
class KettleItemStartLoop(Resource):
    """Retrieve the target temp from the kettle."""

    @api.expect(nsmodelloopstate)
    @api.marshal_with(nsmodelloopstate)
    def put(self, id):
        """Update a kettles target temperature given its identifier."""
        schema = KettleStateSchema()
        kettle = Kettle.get_by_id(id)
        if not kettle:
            api.abort(404, message=f"Kettle {id} doesn't exist")

        data = schema.load(request.get_json(), partial=True)
        if data:
            if data.get("state") is True:
                kettle.start_loop()
                current_app.logger.info(f"{kettle.name}'s control loop started")
                return schema.dump({"state": kettle.is_running})
            if data.get("state") is False:
                kettle.stop_loop()
                current_app.logger.info(f"{kettle.name}'s control loop stopped")
                return schema.dump({"state": False})
        return api.abort(404, message="Invalid Fields. Cannot Update kettle")
