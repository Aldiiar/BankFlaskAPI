from flask import Flask
from kafka_consumer import start_consumer
import threading

app = Flask(__name__)

# Стартуем Kafka consumer в отдельном потоке сразу при запуске
def run_kafka_consumer():
    thread = threading.Thread(target=start_consumer, daemon=True)
    thread.start()

run_kafka_consumer()

if __name__ == "__main__":
    print("[Notification Service] Запуск Flask + Kafka Consumer...")
    app.run(port=5003)
