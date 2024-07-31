from django.core.management.base import BaseCommand
from centerHandling.emailConsumer import EmailKafkaConsumerService

class Command(BaseCommand):
    help = 'Run Kafka consumer for email tasks'

    def handle(self, *args, **kwargs):
        consumer_service = EmailKafkaConsumerService()
        consumer_service.listen()
