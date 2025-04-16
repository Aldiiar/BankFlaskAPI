from models import User
from db_connection import db
from flask import jsonify


def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"id": user.id, "username": user.username, "balance": user.balance}), 200


def get_user_by_phone(phone_number):
    user = User.query.filter_by(phone_number=phone_number).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"id": user.id, "username": user.username, "balance": user.balance}), 200


def update_balance(data):
    user_id = data.get("user_id")
    new_balance = data.get("new_balance")

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.balance = new_balance
    db.session.commit()

    return jsonify({"message": "Balance updated"}), 200
