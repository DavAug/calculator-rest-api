from flask import Flask

from .api import init_history_database


def create_app(testing=False):
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.update({'TESTING': testing})

    with app.app_context():
        from .routes import calculator

        app.register_blueprint(calculator)
        db = init_history_database(app.config['TESTING'])
        app.config.update({'HYSTORY_DB': db})

        return app
