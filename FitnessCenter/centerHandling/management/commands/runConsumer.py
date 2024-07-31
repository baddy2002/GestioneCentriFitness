from django.core.management.base import BaseCommand
from centerHandling.consumer import KafkaConsumerService
from django.conf import settings
class Command(BaseCommand):
    help = 'Run Kafka consumer'

    def handle(self, *args, **kwargs):
        consumer_service = KafkaConsumerService(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS_READERS)
        consumer_service.listen()