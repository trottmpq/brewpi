# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask_execute import Celery
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

csrf_protect = CSRFProtect()
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
celery = Celery()
restx = Api(version="1.0", title="brewpi API", description="Brewpi API", prefix='/api/', doc="/doc/")
