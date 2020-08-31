# -*- coding: utf-8 -*-
"""Temp Sensors views."""
from flask import Blueprint, render_template
from flask_login import login_required

blueprint = Blueprint(
    "tempsensor", __name__, url_prefix="/tempsensors", static_folder="../static"
)


@blueprint.route("/")
@login_required
def themp_sensors():
    """List members."""
    return render_template("heaters/heaters.html")
