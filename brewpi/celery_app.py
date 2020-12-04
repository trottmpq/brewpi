#!/usr/bin/env python
"""Celery Entrypoint for workers."""
from brewpi.app import celery, create_app  # noqa

app = create_app()
app.app_context().push()
