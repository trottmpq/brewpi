"""Celery tasks to be spawned."""
from flask import current_app

from brewpi.extensions import celery

from .. import models


@celery.task
def add(x, y, kettle_id):
    """Example task."""
    current_app.logger.info(f"add {x} and {y}")
    kettle = models.Kettle.get_by_id(kettle_id)
    current_app.logger.info(f"kettle name is {kettle.name}")
    return x + y
