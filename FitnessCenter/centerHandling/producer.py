from kafka import KafkaProducer
import json
from django.conf import settings
from decimal import Decimal
from datetime import datetime, date, time

def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, date):
        return obj.isoformat()
    if isinstance(obj, time):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Type {type(obj)} not serializable")

class KafkaProducerService:
    def __init__(self, bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS_WRITERS):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v, default=serialize_datetime).encode('utf-8')
        )

    def send_employee_invitation(self, topic, data):

        self.producer.send(topic, value=data)
        self.producer.flush()


    def send_email_task(self, data):
        self.send_employee_invitation('email-tasks', data)

    