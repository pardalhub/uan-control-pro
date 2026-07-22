import os

from flask import Flask

from config import Config
from models import db
from routes import main


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    # Corrige a URL do PostgreSQL do Render
    if app.config["SQLALCHEMY_DATABASE_URI"].startswith("postgres://"):
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            app.config["SQLALCHEMY_DATABASE_URI"]
            .replace("postgres://", "postgresql://", 1)
        )

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)

    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)