from kafka import KafkaConsumer
import json
from .models import Employee, Exit
from django.conf import settings
class KafkaConsumerService:
    def __init__(self, bootstrap_servers):
        self.consumer = KafkaConsumer(
            settings.KAFKA_TOPIC_READERS,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS_READERS,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='center-handling-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

    def listen(self):
        for message in self.consumer:
            data = message.value
            self.process_message(data)

    def process_message(self, data):
        employee_uuid = data['employee_uuid']
        status = data['status']
        try:
            employee = Employee.objects.get(uuid=employee_uuid)
            if status == 'accepted':
                employee.is_active = True
                employee.save()
                exit = Exit.objects.filter(employee_uuid=employee.uuid, type='salary').first()
                exit.is_active = True
                exit.save()
            elif status == 'rejected':
                employee.delete()
        except Employee.DoesNotExist:
            print(f"Employee with UUID {employee_uuid} does not exist.")
