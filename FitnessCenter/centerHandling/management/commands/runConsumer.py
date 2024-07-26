from django.core.management.base import BaseCommand
from centerHandling.consumer import KafkaConsumerService

class Command(BaseCommand):
    help = 'Run Kafka consumer'

    def handle(self, *args, **kwargs):
        consumer_service = KafkaConsumerService(bootstrap_servers='localhost:9093')
        consumer_service.listen()