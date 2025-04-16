from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_transaction_event(event_data):
    producer.send('transactions', value=event_data)
    producer.flush()
