# -*- coding: utf-8 -*-
"""API views."""
from flask import Blueprint, render_template

blueprint = Blueprint("main", __name__)

@blueprint.route('/')
def root():
    return render_template('index.html')
