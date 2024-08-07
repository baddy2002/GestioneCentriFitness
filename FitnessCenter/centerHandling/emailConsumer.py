# myapp/email_consumer.py
from kafka import KafkaConsumer
import json
from io import BytesIO
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from weasyprint import HTML
from decimal import Decimal
from django.conf import settings
from .models import Employee
import uuid
from datetime import date, datetime, time
def parse_datetime(value):
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return value

def parse_date(value):
    try:
        return date.fromisoformat(value)
    except ValueError:
        return value

def parse_time(value):
    try:
        return time.fromisoformat(value)
    except ValueError:
        return value

def deserialize_datetime(obj):
    try:
        if isinstance(obj, str):
            if 'T' in obj:  # Simple heuristic to determine datetime vs date vs time
                try:
                    return parse_datetime(obj)
                except ValueError:
                    return obj
            else:
                try:
                    return parse_date(obj)
                except ValueError:
                    return obj
        elif isinstance(obj, float):
            return Decimal(obj)
        return obj
    except Exception as e: 
        print("error deserializing message: " +str(e))
    return None
class EmailKafkaConsumerService:
    def __init__(self):
        self.consumer = KafkaConsumer(
            'email-tasks',
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS_EMAIL_READERS,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='email-task-group',
            value_deserializer=lambda x: self._safe_deserialize(x)
        )

    def _safe_deserialize(self, x):
        try:
            return json.loads(x.decode('utf-8'), object_hook=deserialize_datetime)
        except json.JSONDecodeError as e:
            print(f"Error deserializing message: {e}")
            return {"error": "None or invalid message"}  # Or some default value if applicable
    def listen(self):
        for message in self.consumer:
            data = message.value
            print(data)
            if data['error'] is None:
                self.process_message(data)
            else:
                print("ma come cazzo fa a non arrivarci dio maiale")

    def process_message(self, data):
        try:
            email_type = data['type']
            if email_type == 'customer':
                self.send_customer_email(**data['data'])
            elif email_type == 'employee':
                self.send_employee_email(**data['data'])
        except json.JSONDecodeError as e:
            # Logga l'errore e continua
            print(f"Error deserializing message: {e}")

    def send_customer_email(self, name, prenotation_status, prenotation_total, employee_uuid, executor, availability_moments, new_employee_uuid, recipient_email, prenotation_uuid, server, prenotation_center, prenotation_employee):
        employee = Employee.objects.filter(uuid=uuid.UUID(employee_uuid)).first()
        new_employee = None
        if new_employee_uuid:
            new_employee = Employee.objects.filter(uuid=uuid.UUID(new_employee_uuid)).first()

        context = {
            'name': name,
            'prenotation_status': prenotation_status,
            'prenotation_total': prenotation_total,
            'employee': employee,
            'executor': executor,
            'availability_moments': availability_moments,
            'new_employee': new_employee,
            'prenotation_uuid': prenotation_uuid,
            'server': server,
            'prenotation_center': prenotation_center,
            'prenotation_employee': prenotation_employee
        }

        html_content = render_to_string('deletePrenotationCustomerEmail.html', context)

        # Convert HTML to PDF
        pdf_file = BytesIO()
        HTML(string=html_content).write_pdf(pdf_file)
        pdf_file.seek(0)

        # Create email
        email = EmailMultiAlternatives(
            subject="Prenotation Cancelled",
            body=html_content,  # This is the text version of the email
            from_email=settings.EMAIL_HOST_USER,
            to=[recipient_email]
        )
        email.attach_alternative(html_content, "text/html")  # Set the content as HTML
        email.attach('customerBody.pdf', pdf_file.read(), 'application/pdf')
        email.send()

    def send_employee_email(self, customer_email, prenotation_status, prenotation_from, prenotation_to, employee_name, executor, recipient_email, prenotation_uuid, server):
        print ('server = ' +str(server) )
        context = {
            'customer_email': customer_email,
            'prenotation_status': prenotation_status,
            'prenotation_from': prenotation_from,
            'prenotation_to': prenotation_to,
            'employee_name': employee_name,
            'executor': executor,
            'prenotation_uuid': prenotation_uuid,
            'server': server
        }

        html_content = render_to_string('deletePrenotationEmployeeEmail.html', context)

        # Convert HTML to PDF
        pdf_file = BytesIO()
        HTML(string=html_content).write_pdf(pdf_file)
        pdf_file.seek(0)

        # Create email
        email = EmailMultiAlternatives(
            subject="Prenotation Cancelled",
            body=html_content,  # This is the text version of the email
            from_email=settings.EMAIL_HOST_USER,
            to=[recipient_email]
        )
        email.attach_alternative(html_content, "text/html")  # Set the content as HTML
        email.attach('employeeBody.pdf', pdf_file.read(), 'application/pdf')
        email.send()
