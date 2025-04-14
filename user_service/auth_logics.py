from models import User
from db_connection import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, \
    jwt_required, get_jwt_identity


def register_user(data):
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "User already exists!"}), 400

    new_user = User(
        username=data["username"],
        email=data["email"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        phone_number=data["phone_number"],
        password_hash=generate_password_hash(data["password_hash"])
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!",
                    "user": data}), 201


def login_user(data):
    user = User.query.filter_by(username=data["username"]).first()
    if user and check_password_hash(user.password_hash, data["password_hash"]):

        access_token = create_access_token(identity=user.username)
        refresh_token = create_refresh_token(identity=user.username)

        return jsonify(
            {
                "message": "Login successfully",
                "tokens": {
                    "access": access_token,
                    "refresh": refresh_token
                }
            }
        ), 200
    return jsonify({"message": "Something went wrong!"}), 401


@jwt_required()
def user_profile():
    current_username = get_jwt_identity()
    user = User.query.filter_by(username=current_username).first()

    if not user:
        return jsonify({"error": "User is not found!"}), 404

    return jsonify({
        "username": user.username,
        "phone_number": user.phone_number,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email
    }), 200
