from flask import Flask


def create_app():
    """Application factory for the Fleet Mix Flask app."""
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="dev",  # replace with a random value before deployment
    )

    from . import routes

    app.register_blueprint(routes.bp)

    return app
