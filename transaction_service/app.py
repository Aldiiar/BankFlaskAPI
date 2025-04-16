from flask import Flask, request
from configuration import Config
from db_connection import db, jwt
from models import Transaction
from flask_migrate import Migrate
from transaction_logics import create_transaction


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    Migrate(app, db)

    @app.route("/send_money", methods=["POST"])
    def send_money():
        data = request.get_json()
        return create_transaction(data)

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(port=5002)
