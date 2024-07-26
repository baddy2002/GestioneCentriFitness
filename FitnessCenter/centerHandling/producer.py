from kafka import KafkaProducer
import json
from django.conf import settings
class KafkaProducerService:
    def __init__(self, bootstrap_servers):
        self.producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS_WRITERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def send_employee_invitation(self, topic, data):
        self.producer.send(topic, value=data)
        self.producer.flush()