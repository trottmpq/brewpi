# -*- coding: utf-8 -*-
"""API views."""
from flask import Blueprint
from flask_restx import Api


from .recipe import api as recipens

blueprint = Blueprint("recipes", __name__, url_prefix="/recipes")

api = Api(
    blueprint,
    title="Recipes",
    version="1.0",
    description="Api to control all the various devices in the brewery",
)

api.add_namespace(recipens)

