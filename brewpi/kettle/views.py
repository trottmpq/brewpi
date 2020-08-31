# -*- coding: utf-8 -*-
"""Kettle views."""
from flask import Blueprint, render_template
from flask_login import login_required

blueprint = Blueprint(
    "kettle", __name__, url_prefix="/kettles", static_folder="../static"
)


@blueprint.route("/")
@login_required
def kettles():
    """List members."""
    return render_template("heaters/heaters.html")
