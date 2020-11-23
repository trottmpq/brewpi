# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import logging
import sys

from flask import Flask, render_template, jsonify
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
    register_config(app)

    with app.app_context():
        @app.route('/')
        def index():
            return render_template('index.html')

    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    ma.init_app(app)
    csrf_protect.init_app(app)
    migrate.init_app(app, db)
    celery.init_app(app)
    restx.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(devices.views.blueprint, url_prefix="/api/devices")
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


def register_config(app):
    app.brewpi_config = dict()
    app.brewpi_config["Devices"] = dict()
    app.brewpi_config["Devices"]["TempSensors"] = dict()
    app.brewpi_config["Devices"]["Heaters"] = dict()
    app.brewpi_config["Devices"]["Pumps"] = dict()
    with app.app_context():
        for tempsensor in devices.models.TempSensor.query.all():
            app.brewpi_config["Devices"]["TempSensors"][tempsensor.id] = {
                "name": tempsensor.name,
                "gpio_num": tempsensor.gpio_num,
                "active_low": tempsensor.active_low}
        for heater in devices.models.Heater.query.all():
            app.brewpi_config["Devices"]["Heaters"][heater.id] = {
                "name": heater.name,
                "gpio_num": heater.gpio_num,
                "active_low": heater.active_low}
        for pump in devices.models.Pump.query.all():
            app.brewpi_config["Devices"]["Pumps"][pump.id] = {
                "name": pump.name,
                "gpio_num": pump.gpio_num,
                "active_low": pump.active_low}
    print(app.brewpi_config)



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
