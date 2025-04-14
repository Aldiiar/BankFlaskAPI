from flask import Flask, request
from configuration import Config
from db_connection import db, jwt
from auth_logics import register_user, login_user, user_profile
from models import User
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    Migrate(app, db)

    @app.route("/register", methods=["POST"])
    def registration():
        data = request.get_json()

        return register_user(data)


    @app.route("/login", methods=["POST"])
    def login():
        data = request.get_json()

        return login_user(data)


    @app.route("/profile", methods=["GET"])
    def get_profile():
        return user_profile()


    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(port=5001)
