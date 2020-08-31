# -*- coding: utf-8 -*-
"""Temp Sensor forms."""
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired, Length, NumberRange

from .models import TempSensor


class TempSensorForm(FlaskForm):
    """Register form."""

    name = StringField("name", validators=[DataRequired(), Length(min=3, max=25)])
    gpio_num = IntegerField(
        "GPIO Number",
        validators=[
            DataRequired(),
            NumberRange(min=1, max=16, message="GPIO must be between 1 and 16"),
        ],
    )

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(TempSensorForm, self).__init__(*args, **kwargs)
        self.name = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(TempSensorForm, self).validate()
        if not initial_validation:
            return False
        tempsense = TempSensor.query.filter_by(name=self.name.data).first()
        if tempsense:
            self.name.errors.append("Name already exists")
            return False
        tempsense = TempSensor.query.filter_by(gpio_num=self.gpio_num.data).first()
        if tempsense:
            self.gpio_num.errors.append("GPIO is already assigned")
            return False
        return True
