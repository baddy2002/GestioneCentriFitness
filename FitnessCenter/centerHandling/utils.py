from datetime import datetime, date, timedelta
from dateutil import parser
import re
import uuid
from .models import Employee

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
    def generate_slots(cls, start_time, end_time, date=None):
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
            next_time = current_time + timedelta(minutes=30)
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
        employee  =Employee.objects.filter(uuid=uuid.UUID(employee_uuid)).first()
        new_employee = None
        if new_employee_uuid:
            print('second')
            new_employee = Employee.objects.filter(uuid=uuid.UUID(new_employee_uuid)).first()
        if executor == 'customer':
            print('third')
            print("Hi "+ str(name))
            print (f"your prenotation with {employee.first_name} {employee.last_name}  of total: {prenotation_total} is succesfully:" +str(prenotation_status))

        else:
            print("Hi "+ str(name))
            print(f'We are sorry to inform you that your prenotation with {employee.first_name} {employee.last_name} was deleted because the {employee.type} is no more available')
            if new_employee:
                print(f"We found as substitute: {new_employee.first_name} {new_employee.last_name}, you can accept or decline this prenotation!")
                print(f"this are the first available moments of your original {employee.type}:")
                print(availability_moments.get('employee_availability'))
                
            else:
                print(f'We was not able to find a substitute, here you can see the first available moments for your {employee.type}')
                print(availability_moments.get('employee_availability'))
                print(f"alternativally you can choice another {employee.type} of the center:")
                print(availability_moments.get('center_availability'))
            print("Please choice if accept or decline the coices")
    
    
    @classmethod
    def generate_employee_content(cls, customer_email, prenotation_status, prenotation_from, prenotation_to, employee_name, executor):
        
        if executor != 'customer':
            print("Hi "+ str(employee_name))
            print (f"your prenotation from {prenotation_from} to {prenotation_to} is succesfully updated: {prenotation_status} we already inform customer to his email: {customer_email}")

        else:
            print("Hi "+ str(employee_name))
            print(f'customer: {customer_email} cancel his prenotation to with you on {prenotation_from} - {prenotation_to}')

