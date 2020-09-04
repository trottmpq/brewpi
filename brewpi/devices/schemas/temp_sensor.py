"""Temperature schemas."""

from brewpi.extensions import ma

from ..models import TempSensor


class TempSensorSchema(ma.SQLAlchemyAutoSchema):
    """A Temperature Sensor Schema."""

    class Meta:
        """A Temperature Sensor Schema Metaclass."""

        model = TempSensor


class TempSensorTempSchema(ma.SQLAlchemyAutoSchema):
    """A Temperature Sensor Schema."""

    class Meta:
        """A Temperature Sensor Schema Metaclass."""

        model = TempSensor
        fields = ["temperature"]
