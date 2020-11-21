# -*- coding: utf-8 -*-
"""API views."""
from flask import Blueprint

blueprint = Blueprint("main", __name__)

@blueprint.route('/')
def root():
    return blueprint.send_static_file('index.html')
