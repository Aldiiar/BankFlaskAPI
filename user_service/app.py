from flask import Flask, request
from configuration import Config
from db_connection import db, jwt
from auth_logics import register_user, login_user, user_profile
from users_logics import get_user_by_phone, get_user_by_id, update_balance
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

    @app.route("/users/<int:user_id>", methods=["GET"])
    def get_users_data(user_id):
        return get_user_by_id(user_id)

    @app.route("/users/by_phone/<string:phone_number>", methods=["GET"])
    def get_user_by_phone_route(phone_number):
        return get_user_by_phone(phone_number)

    @app.route("/users/update_balance", methods=["POST"])
    def update_user_balance():
        data = request.get_json()

        return update_balance(data)

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(port=5001)
