from kafka import KafkaConsumer
import json
import threading

def handle_event(event):
    sender = event.get("sender_id")
    receiver = event.get("receiver_id")
    amount = event.get("amount")
    status = event.get("status")
    sender_balance = event.get("sender_balance")
    receiver_balance = event.get("receiver_balance")

    if status == "pending":
        print(f"[Notification] Платеж от пользователя {sender} на сумму {amount} в обработке...")
    elif status == "completed":
        print(f"[Notification] Пользователь {receiver}, ваш баланс пополнен на {amount} cом!\n"
              f"Ваш текущий баланс: {receiver_balance}")
        print(f"[Notification] Платеж завершен. С баланса пользователя {sender} списано {amount} cом.\n"
              f"Ваш текущий баланс: {sender_balance}")

def start_consumer():
    def consume():
        consumer = KafkaConsumer(
            'transactions',
            bootstrap_servers='localhost:9092',
            group_id='notification-group',
            auto_offset_reset='earliest'
        )

        for message in consumer:
            event = json.loads(message.value.decode('utf-8'))
            handle_event(event)

    threading.Thread(target=consume, daemon=True).start()
