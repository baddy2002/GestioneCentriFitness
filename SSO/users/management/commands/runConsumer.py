from django.core.management.base import BaseCommand
from users.consumer import KafkaConsumerService

class Command(BaseCommand):
    help = 'Run Kafka consumer'

    def handle(self, *args, **kwargs):
        consumer_service = KafkaConsumerService(bootstrap_servers='sso-kafka-1:9092')
        consumer_service.listen()