from models import Transaction
from db_connection import db
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests
from configuration import Config
from kafka_producer import send_transaction_event

@jwt_required()
def create_transaction(data):
    current_user_id = get_jwt_identity()
    token = request.headers.get('Authorization').split()[1]
    headers = {"Authorization": f"Bearer {token}"}

    amount = data.get("amount")
    receiver_phone = data.get("receiver_phone")

    if not amount or not receiver_phone:
        return jsonify({"error": "Missing fields"}), 400

    # Получаем отправителя
    sender_resp = requests.get(f"{Config.USER_SERVICE_URL}/users/{current_user_id}", headers=headers)
    if sender_resp.status_code != 200:
        return jsonify({"error": "Sender not found"}), 404
    sender_data = sender_resp.json()
    sender_balance = sender_data["balance"]

    if sender_balance < amount:
        return jsonify({"error": "Insufficient funds"}), 400

    # Получаем получателя
    receiver_resp = requests.get(f"{Config.USER_SERVICE_URL}/users/by_phone/{receiver_phone}", headers=headers)
    if receiver_resp.status_code != 200:
        return jsonify({"error": "Receiver not found"}), 404
    receiver_data = receiver_resp.json()
    receiver_id = receiver_data["id"]
    receiver_balance = receiver_data["balance"]

    # 📡 Отправляем событие "pending"
    send_transaction_event({
        "sender_id": current_user_id,
        "receiver_id": receiver_id,
        "amount": amount,
        "status": "pending"
    })

    # Обновляем балансы
    sender_new_balance = sender_balance - amount
    receiver_new_balance = receiver_balance + amount

    requests.post(f"{Config.USER_SERVICE_URL}/users/update_balance", json={
        "user_id": current_user_id,
        "new_balance": sender_new_balance
    }, headers=headers)

    requests.post(f"{Config.USER_SERVICE_URL}/users/update_balance", json={
        "user_id": receiver_id,
        "new_balance": receiver_new_balance
    }, headers=headers)

    # Сохраняем транзакцию
    transaction = Transaction(sender_id=current_user_id, receiver_id=receiver_id, amount=amount)
    db.session.add(transaction)
    db.session.commit()

    # 📡 Отправляем событие "completed"
    send_transaction_event({
        "sender_id": current_user_id,
        "receiver_id": receiver_id,
        "amount": amount,
        "sender_balance": sender_new_balance,
        "receiver_balance": receiver_new_balance,
        "status": "completed"
    })

    return jsonify({"message": "Transaction completed!"}), 201
