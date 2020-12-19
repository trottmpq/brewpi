# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import logging
import sys

from flask import Flask, jsonify, render_template
from flask_wtf.csrf import CSRFError

from brewpi import commands, devices, recipes
from brewpi.extensions import celery, csrf_protect, db, ma, migrate, restx


def create_app(config_object="brewpi.settings"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    configure_logger(app)
    init_celery(app)

    with app.app_context():

        @app.route("/")
        def index():
            return render_template("index.html")

    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    ma.init_app(app)
    csrf_protect.init_app(app)
    migrate.init_app(app, db)
    restx.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(devices.blueprint, url_prefix="/api/devices")
    app.register_blueprint(recipes.views.blueprint, url_prefix="/api/recipes")
    return None


def register_errorhandlers(app):
    """Register error handlers."""

    @app.errorhandler(401)
    @app.errorhandler(404)
    @app.errorhandler(500)
    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return jsonify(error=str(error_code)), error_code

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return jsonify(reason=e.description), 400

    return None


def init_celery(app=None):
    """Setup celery with an app context."""
    app = app or create_app()
    celery.conf.update(app.config)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        """Make celery tasks work with Flask app context."""

        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    celery.conf.beat_schedule = {
        "add-every-1-second": {
            "task": "brewpi.devices.tasks.update_temperature",
            "schedule": 1.0,
        },
    }

    return celery


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {"db": db}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)
