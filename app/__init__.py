from flask import Flask


def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)

    with app.app_context():
        from .routes import calculator

        app.register_blueprint(calculator)

        return app
