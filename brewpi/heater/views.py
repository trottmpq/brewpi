# -*- coding: utf-8 -*-
"""Heater views."""
from flask import Blueprint, render_template
from flask_login import login_required

blueprint = Blueprint(
    "heater", __name__, url_prefix="/heaters", static_folder="../static"
)


@blueprint.route("/")
@login_required
def heaters():
    """List members."""
    return render_template("heaters/heaters.html")
