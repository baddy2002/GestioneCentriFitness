from datetime import datetime, date, timedelta
from dateutil import parser
import re
import uuid
from .models import Employee
from django.template.loader import render_to_string
from weasyprint import HTML

class DateUtils():
    
    date_patterns = [
            re.compile(r'^\d{4}-\d{2}-\d{2}$'),  # yyyy-MM-dd
            re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'),  # yyyy-MM-dd'T'HH:mm:ss
            re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$'),  # yyyy-MM-dd'T'HH:mm:ss.SSSZ
            re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.+\d{2}:\d{2}$')  # yyyy-MM-dd'T'HH:mm:ss.SSSZ
        ]

    @classmethod
    def parse_string_to_date(cls, s):
        if any(pattern.match(s) for pattern in cls.date_patterns):
            # Usa dateutil per parsare la stringa in un oggetto datetime
            dt = parser.parse(s)
            # Ritorna solo la parte di data (yyyy-MM-dd)
            return dt.date()
        else:
            raise ValueError("Date format is not supported")
        

    @classmethod
    def parse_string_to_datetime(cls, s):
        if any(pattern.match(s) for pattern in cls.date_patterns):
            
            dt = parser.parse(s)

            return dt
        else:
            raise ValueError("Date format is not supported")
        
    @classmethod
    def generate_slots(cls, start_time, end_time, date=None, duration = 30):
        # Converti start_time e end_time in datetime.datetime per la manipolazione
        if date == None:
            date = datetime.now().date()
        start_datetime = datetime.combine(date, start_time)
        end_datetime = datetime.combine(date, end_time)
        
        # Validazione degli orari
        if start_datetime >= end_datetime:
            raise ValueError("L'orario di inizio deve essere precedente all'orario di fine.")
        
        # Crea una lista per gli intervalli di mezz'ora
        slots = []
        
        current_time = start_datetime
        while current_time < end_datetime:
            next_time = current_time + timedelta(minutes=duration)
            slots.append((current_time.time(), next_time.time()))
            current_time = next_time
        
        return slots


class PaymentsUtils():
    @classmethod
    def pay(cls):
        return

    @classmethod
    def refund(cls):
        return

class EmailsUtils():
    @classmethod
    async def send(cls, content, to, cc, sender, subject):
        return

    @classmethod
    def generate_customer_content(cls, name, prenotation_status, prenotation_total, employee_uuid, executor, availability_moments=None, new_employee_uuid=None):
        employee  = Employee.objects.filter(uuid=uuid.UUID(employee_uuid)).first()
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
            'new_employee': new_employee
        }
        
        html_content = render_to_string('deletePrenotationCustomerEmail.html', context)

        # Convert HTML to PDF
        pdf_file = HTML(string=html_content).write_pdf()
        
        # Save PDF to file
        with open('customerBody.pdf', 'wb') as file:
            file.write(pdf_file)
          

    @classmethod
    def generate_employee_content(cls, customer_email, prenotation_status, prenotation_from, prenotation_to, employee_name, executor):
        
        context = {
            'customer_email': customer_email,
            'prenotation_status': prenotation_status,
            'prenotation_from': prenotation_from,
            'prenotation_to': prenotation_to,
            'employee_name': employee_name,
            'executor': executor
        }
        
        html_content = render_to_string('deletePrenotationEmployeeEmail.html', context)
        
        # Convert HTML to PDF
        pdf_file = HTML(string=html_content).write_pdf()
        
        # Save PDF to file
        with open('employeeBody.pdf', 'wb') as file:
            file.write(pdf_file)