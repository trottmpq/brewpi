# -*- coding: utf-8 -*-
"""API views."""
from flask import Blueprint

blueprint = Blueprint("main", __name__, static_folder='../reactbrew/build')

@blueprint.route('/')
def root():
    return blueprint.send_static_file('index.html')
