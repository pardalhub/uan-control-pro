import os

from flask import Flask
from flask_login import LoginManager

from config import Config
from models import db, Usuario
from routes import main

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuario, int(user_id))


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    if app.config["SQLALCHEMY_DATABASE_URI"].startswith("postgres://"):
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            app.config["SQLALCHEMY_DATABASE_URI"]
            .replace("postgres://", "postgresql://", 1)
        )

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)

    login_manager.login_view = "main.login"
    login_manager.init_app(app)

    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

        if Usuario.query.count() == 0:
            admin = Usuario(
                nome="Administrador",
                email="admin@uan.com",
                perfil="Administrador"
            )

            admin.set_senha("123456")

            db.session.add(admin)
            db.session.commit()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)