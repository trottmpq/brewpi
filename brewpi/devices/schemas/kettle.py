"""Heater schemas."""

from brewpi.extensions import ma

from ..models import Kettle


class KettleSchema(ma.SQLAlchemyAutoSchema):
    """A Heater Schema."""

    class Meta:
        """A Heater Schema Metaclass."""

        model = Kettle
        include_fk = True
        # fields = ('name', 'heater_id', 'tempsense_id')
