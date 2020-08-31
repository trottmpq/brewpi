# -*- coding: utf-8 -*-
"""Kettle forms."""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

from .models import Kettle


class KettleForm(FlaskForm):
    """Register form."""

    name = StringField("name", validators=[DataRequired(), Length(min=3, max=25)])

    def __init__(self, *args, **kwargs):
        """Create KettleForm."""
        super(KettleForm, self).__init__(*args, **kwargs)
        self.name = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(KettleForm, self).validate()
        if not initial_validation:
            return False
        kettle = Kettle.query.filter_by(name=self.name.data).first()
        if kettle:
            self.name.errors.append("Name already exists")
            return False
        return True
