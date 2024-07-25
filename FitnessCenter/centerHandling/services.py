from .models import Employee
from .serializers import ExitSerializer
import uuid
from .producer import KafkaProducerService
from .utils import DateUtils

class EmployeeService:
    def __init__(self):
        self.kafka_producer = KafkaProducerService(bootstrap_servers='localhost:9092')

    def send_invitation(self, employee_email, employee_uuid):
        #TODO: Logic of invitation on an employee
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
        self.send_invitation(employee.email ,employee.uuid)            #TODO: handle invation


    def get_search(self, query_params):
        employees = Employee.objects.all()

        order_by = query_params.get('orderBy', '-hiring_date')
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

        employees = employees.all().order_by(order_by)
        
        return employees  