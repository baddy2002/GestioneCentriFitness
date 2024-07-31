from urllib.parse import unquote
from .models import Center, Employee, EmployeeBusyTrace
from .serializers import ExitSerializer, PrenotationSerializer
import uuid
from .producer import KafkaProducerService
from .utils import DateUtils
from django.db.models import Q
import requests
from django.conf import settings

class EmployeeService:
    def __init__(self):
        self.kafka_producer = KafkaProducerService(bootstrap_servers='localhost:9092')

    def send_invitation(self, employee_email, employee_uuid):
        data = {
            'email': employee_email,
            'employee_uuid': str(employee_uuid)
        }
        self.kafka_producer.send_employee_invitation('employee-invitation', data)

    def post_persist_employee(self, employee):
        exit_data = {
            'uuid': uuid.uuid4(),
            'type': 'salary',
            'amount': employee.salary,
            'description': f'salary per month of employee {employee.get_full_name()}',
            'frequency': 1,
            'center_uuid': employee.center_uuid,
            'employee_uuid': str(employee.uuid),
            'start_date': employee.hiring_date,
            'expiration_date': employee.end_contract_date,
            'is_active': False
        }
        exit_serializer = ExitSerializer(data=exit_data)
        if exit_serializer.is_valid():
            exit_serializer.save()
        else:
            print(exit_serializer.errors)  
        self.send_invitation(employee.email ,employee.uuid)          

    def get_search(self, query_params):
        employees = Employee.objects.all()

        if query_params.get('orderBy'):
            order_by = unquote(query_params.get('orderBy'))
        else:
            order_by = '-hiring_date'
        if query_params.get('obj.manager_id') is not None:
            centers = Center.objects.filter(manager_id=query_params.get('obj.manager_id'))
            center_uuids = [center_uuid for center_uuid in centers.values_list(str('uuid'), flat=True)]
            center_uuids = [str(uuid) for uuid in center_uuids]
            employees = employees.filter(center_uuid__in=center_uuids)
        if query_params.get('obj.uuid') is not None:
            employees=employees.filter(uuid=query_params.get('obj.uuid'))
        if query_params.get('like.first_name') is not None:
            employees=employees.filter(first_name__icontains=query_params.get('like.first_name'))
        if query_params.get('like.last_name') is not None:
            employees=employees.filter(last_name__icontains=query_params.get('like.last_name'))
        if query_params.get('from.DOB') is not None:
            employees=employees.filter(DOB__gte=DateUtils.parse_string_to_date(query_params.get('from.DOB')))
        if query_params.get('to.DOB') is not None:
            employees=employees.filter(DOB__lte=DateUtils.parse_string_to_date(query_params.get('to.DOB')))
        if query_params.get('obj.DOB') is not None:
            employees=employees.filter(DOB=DateUtils.parse_string_to_date(query_params.get('obj.DOB')))
        if query_params.get('obj.salary') is not None:
            employees=employees.filter(float=float(query_params.get('obj.salary')))
        if query_params.get('like.fiscalCode') is not None:
            employees=employees.filter(fiscalCode__icontains=query_params.get('like.fiscalCode'))
        if query_params.get('obj.type') is not None:
            employees=employees.filter(type=query_params.get('obj.type'))
        if query_params.get('from.hiring_date') is not None:
            employees=employees.filter(hiring_date__gte=DateUtils.parse_string_to_date(query_params.get('from.hiring_date')))
        if query_params.get('to.hiring_date') is not None:
            employees=employees.filter(hiring_date__lte=DateUtils.parse_string_to_date(query_params.get('to.hiring_date')))
        if query_params.get('obj.hiring_date') is not None:
            employees=employees.filter(hiring_date=DateUtils.parse_string_to_date(query_params.get('obj.hiring_date')))
        if query_params.get('from.end_contract_date') is not None:
            employees=employees.filter(end_contract_date__gte=DateUtils.parse_string_to_date(query_params.get('from.end_contract_date')))
        if query_params.get('to.end_contract_date') is not None:
            employees=employees.filter(end_contract_date__lte=DateUtils.parse_string_to_date(query_params.get('to.end_contract_date')))
        if query_params.get('obj.end_contract_date') is not None:
            employees=employees.filter(end_contract_date=DateUtils.parse_string_to_date(query_params.get('obj.end_contract_date')))
        if query_params.get('obj.center_uuid') is not None:
            employees=employees.filter(center_uuid=query_params.get('obj.center_uuid'))
        if query_params.get('obj.is_active') is not None and query_params.get('obj.is_active').strip().lower() == 'false':
            employees=employees.filter(is_active=False)
        else:
            employees=employees.filter(is_active=True)

        employees = employees.all().order_by(*order_by.split(','))
        
        return employees  
    
class PrenotationService:
    @classmethod
    def replaceEmployee(cls, prenotation):
        serializer = PrenotationSerializer()
        new_empolyee_uuid = serializer.find_best_employee(center_uuid=prenotation.center_uuid, type=prenotation.type,
                                       from_hour=prenotation.from_hour, to_hour=prenotation.to_hour)

        if new_empolyee_uuid:
            prenotation.employee_uuid = new_empolyee_uuid
            prenotation.save()
            return new_empolyee_uuid
        else:
            return None
        

    @classmethod
    def find_next_available_moments(cls, prenotation):

        print(f'{settings.BACKEND_SERVICE_PROTOCOL}://{settings.BACKEND_SERVICE_DOMAIN}:{settings.BACKEND_SERVICE_PORT}/api/availability/{prenotation.type}/{prenotation.from_hour.date()}/{prenotation.center_uuid}')
        response1 = requests.get(f'{settings.BACKEND_SERVICE_PROTOCOL}://{settings.BACKEND_SERVICE_DOMAIN}:{settings.BACKEND_SERVICE_PORT}/api/availability/{prenotation.type}/{prenotation.from_hour.date()}/{prenotation.center_uuid}')
        response2 = requests.get(f'{settings.BACKEND_SERVICE_PROTOCOL}://{settings.BACKEND_SERVICE_DOMAIN}:{settings.BACKEND_SERVICE_PORT}/api/availability/{prenotation.type}/{prenotation.from_hour.date()}/{prenotation.center_uuid}/{prenotation.employee_uuid}')
        if response1 and response1.json() and response2 and response2.json(): 
            center_availability = response1.json().get('availability')
            employee_availability = response2.json().get('availability')
            if center_availability and len(center_availability) > 0:
                center_availability = center_availability[0:5]
            if employee_availability and len(employee_availability) > 0:
                employee_availability = employee_availability[0:5]
        else:
            raise Exception(f"Error calculating the available moments, response1: {response1} \n response2: {response2}")
        
        return {"center_availability": center_availability, "employee_availability": employee_availability}