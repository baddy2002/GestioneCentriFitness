from kafka import KafkaConsumer
import json
import uuid
from .models import Invito, UserAccount
from django.utils import timezone
from django.conf import settings

class KafkaConsumerService:
    def __init__(self, bootstrap_servers):
        self.consumer = KafkaConsumer(
            settings.KAFKA_TOPIC_READERS,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS_READERS,
            group_id='sso_group',
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
    def listen(self):
        for message in self.consumer:
            self.process_message(message.value)

    def process_message(self, message):
        email = message.get('email')
        employee_uuid = message.get('employee_uuid')
        print("data: "+str(message))
        # Verifica esistenza utente e creazione invito
        user = UserAccount.objects.filter(email=email).first()
        if user:
            invito = Invito(
                uuid=uuid.uuid4(),
                email=email,
                employee_uuid=employee_uuid,
                exec_time=timezone.now(),
                status='pending'
            )
            invito.save()
        else:
            print(f"User with email {email} not found.")
