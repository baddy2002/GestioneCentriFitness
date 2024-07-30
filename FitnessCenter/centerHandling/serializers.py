# serializers.py
from .tokenService import get_principal
from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import Employee, EmployeeBusyTrace, Exit, Center, Prenotation, Review
import re
import uuid
from django.db import models
from django.utils import timezone
import datetime
import requests

class EmployeeSerializer(serializers.ModelSerializer):
    attachments_uuid = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    end_contract_date = serializers.DateField(required=False, allow_null=True)
    class Meta:
        model = Employee
        fields = ['uuid', 'first_name', 'email', 'last_name', 'DOB', 'salary','fiscalCode', 'type', 'center_uuid', 'hiring_date', 'end_contract_date', 'attachments_uuid', 'is_active']

    def validate_end_contract_date(self, value):
        if value is not None:
            if value < timezone.now().date():
                raise serializers.ValidationError("End of contract cannot be in the past.")
        return value


    def validate_fiscalCode(self, value):
        # Controllo che il codice fiscale sia valido (esempio: solo lettere e numeri, lunghezza 16)
        if not re.match(r'^[A-Z0-9]{16}$', value):
            raise serializers.ValidationError("Fiscal code not valid. It should be long only 16 and contain alphanumeric characters only.")
        return value

    def validate_type(self, value):
        # Controllo che il tipo sia 'trainer' o 'nutritionist'
        if value not in ['trainer', 'nutritionist', 'mixed']:
            raise serializers.ValidationError("Type should be trainer, nutritionist or mixed only.")
        return value

    def validate_salary(self, value):
        if value < 0:
            raise serializers.ValidationError("Salary cannot be negative.")
        return value
    
    def validate_center_uuid(self, value):
        center = Center.objects.filter(pk=value).first()

        if center is None:
            raise serializers.ValidationError("Center with this center_uuid does not exist.")
        
        return value

    def validate(self, data):
        # Ensure expiration_date is not earlier than hiring_date if expiration_date is provided
        hiring_date = data.get('hiring_date')
        end_contract_date = data.get('end_contract_date')
        
        if end_contract_date is not None and hiring_date is not None:
            if end_contract_date < hiring_date:
                raise serializers.ValidationError("End contract date cannot be earlier than hiring date.")
        
        return data

class ExitSerializer(serializers.ModelSerializer):
    employee_uuid = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    expiration_date = serializers.DateField(required=False, allow_null=True)
    class Meta:
        model = Exit
        fields = ['uuid', 'amount', 'type', 'description', 'frequency', 'center_uuid', 'employee_uuid', 'start_date', 'expiration_date', 'is_active']

    def validate_expiration_date(self, value):
        # Ensure expiration_date is not a past date
        if value is not None:
            if value < timezone.now().date():
                raise serializers.ValidationError("Expiration date cannot be in the past.")
        return value

    def validate_type(self, value):
        # Controllo che il tipo sia 'trainer' o 'nutritionist'
        if value not in ['salary', 'tax', 'single']:
            raise serializers.ValidationError("Type should be salary, tax or single only.")
        return value

    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Amount cannot be negative.")
        return value

    def validate_frequency(self, value):
        if value < 0:
            raise serializers.ValidationError("Frequency cannot be negative.")
        return value
    
    def validate_center_uuid(self, value):
        center = Center.objects.filter(pk=value).first()

        if center is None:
            raise serializers.ValidationError("Center with this center_uuid does not exist.")
        
        return value

    def validate(self, data):
        # Ensure expiration_date is not earlier than hiring_date if expiration_date is provided
        # Ensure that if the type is 'salary' the employee_uuid should be exist
        start_date = data.get('start_date')
        expiration_date = data.get('expiration_date')

        exit_type = data.get('type')

        if exit_type == 'salary':
            if data.get('frequency') != 1:
                raise serializers.ValidationError("The salary's frequency should be once per month.")
            
            employee = Employee.objects.filter(pk=data.get('employee_uuid')).first()

            if employee is None:
                raise serializers.ValidationError("Employee with this employee_uuid does not exist.")

        
        if expiration_date is not None and start_date is not None:
            if expiration_date < start_date:
                raise serializers.ValidationError("Expiration date cannot be earlier than hiring date.")
        
        return data
    

class CenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Center
        fields = [
            'uuid',
            'name',
            'description',
            'manager_id',
            'province',
            'city',
            'hour_nutritionist_price',
            'hour_trainer_price',
            'street',
            'house_number',
            'is_active',
        ]
        read_only_fields = ['uuid']

    def validate(self, data):
        if self.instance is not None:
            uuid = self.instance.uuid
        province = data.get('province')
        city = data.get('city')
        street = data.get('street')
        house_number = data.get('house_number')
        center = Center.objects.filter(province=province, city=city, street=street, house_number=house_number).first()
        
        if center is not None:
            if self.instance is None and center.is_active==True:                                       #è una post 
                raise serializers.ValidationError("There is another center in this location ! ")
            else:    
                if self.instance is not None and center.uuid != uuid and center.is_active==True:                                        #è una put in cui modifico il luogo e provo a metterlo in uno in cui un negozio esiste già
                    raise serializers.ValidationError("There is another center in this location ! ")
        return data
    

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'uuid',
            'text',
            'score',
            'user_id',
            'center_uuid',
            'exec_time',
            'is_active',
        ]


    def validate_center_uuid(self, value):
        center = Center.objects.filter(pk=value).first()

        if center is None:
            raise serializers.ValidationError("Center with this center_uuid does not exist.")
        
        return value

    def validate(self, data):
        #TODO: implementare filtri per contenuti dannosi
        return data
    

class PrenotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prenotation
        fields = '__all__'

    def validate(self, data):
        # Get the request object to access headers
        request = self.context.get('request')
        if not request:
            raise ValidationError('Request object is missing.')

        # 0. Required fields validation
        for field in ['user_id', 'center_uuid', 'from_hour', 'to_hour', 'type']:
            if not data.get(field):
                raise ValidationError(f'{field} cannot be null.')

        # 1. Validate employee
        employee_uuid = data.get('employee_uuid')
        if employee_uuid:
            employee = Employee.objects.filter(uuid=uuid.UUID(employee_uuid)).first()
            if not employee or not employee.is_active:
                raise ValidationError('Invalid or inactive employee.')

            if employee.type != data.get('type'):
                raise ValidationError('Employee type does not match the prenotation type.')

        # 2. Validate center
        center_uuid = data.get('center_uuid')
        if center_uuid:
            center = Center.objects.filter(uuid=uuid.UUID(center_uuid)).first()
            if not center or not center.is_active:
                raise ValidationError('Invalid or inactive center.')

        # 3. Validate user ID from token
        token = request.headers.get('Authorization')
        if token:
            # Here you need to implement your token parsing logic.
            # This is a placeholder, replace it with actual token parsing.
            user_id_from_token = get_principal(token)
            if user_id_from_token != data.get('user_id'):
                raise ValidationError('User ID in token does not match the user ID in prenotation.')

        # 4. Validate from_hour
        now = timezone.now()
        if data['from_hour'] <= now + datetime.timedelta(days=1):
            raise ValidationError('from_hour must be at least 1 day from now.')

        if data['from_hour'].minute % 30 != 0:
            raise ValidationError('from_hour must be on the half-hour.')

        # 5. Validate to_hour
        if data['to_hour'] <= data['from_hour'] + datetime.timedelta(minutes=30):
            raise ValidationError('to_hour must be at least 30 minutes later than from_hour.')

        if data['to_hour'] >= data['from_hour'] + datetime.timedelta(minutes=150):
            raise ValidationError('the visite cannot last for more than 2h 30 minutes.')

        if data['to_hour'].minute % 30 != 0:
            raise ValidationError('to_hour must be on the half-hour.')

        # 6. Check availability
        if employee_uuid:
            if not self.is_employee_available(employee_uuid, data['from_hour'], data['to_hour']):
                raise ValidationError('Employee is not available during the selected time.')

        elif center_uuid:
            available_employee = self.find_best_employee(center_uuid, data['type'], data['from_hour'], data['to_hour'])
            if available_employee:
                data['employee_uuid'] = available_employee.uuid
                data['total'] = self.calculate_total_price(data['type'], data['from_hour'], data['to_hour'], center_uuid)
                data['status'] = 'confirmed'
            else:
                raise ValidationError('No available employees for the center.')

        return data

    def is_employee_available(self, employee_uuid, from_hour, to_hour):
        overlapping_prenotations = Prenotation.objects.filter(
            employee_uuid=employee_uuid,
            from_hour__lt=to_hour,
            to_hour__gt=from_hour
        ).exists()
        return not overlapping_prenotations

    def find_best_employee(self, center_uuid, type, from_hour, to_hour):
        employees = Employee.objects.filter(center_uuid=center_uuid, type=type, is_active=True)
        best_employee = None
        min_busy_hours = float('inf')
        
        busy_traces = EmployeeBusyTrace.objects.filter(
            employee_uuid__in=employees.values_list('uuid', flat=True)).values('employee_uuid', 'prenotation_hours')
        busy_hours_map = {trace['employee_uuid']: trace['prenotation_hours'] for trace in busy_traces}
        
        for employee in employees:
            if self.is_employee_available(employee.uuid, from_hour, to_hour):
                busy_hours = busy_hours_map.get(employee.uuid, 0)
                if busy_hours < min_busy_hours:
                    min_busy_hours = busy_hours
                    best_employee = employee
        return best_employee

    def calculate_total_price(self, type, from_hour, to_hour, center_uuid):
        center = Center.objects.filter(uuid=uuid.UUID(center_uuid)).first()
        if not center:
            raise ValidationError('Invalid center.')
        duration_hours = (to_hour - from_hour).total_seconds() / 3600
        if type == 'nutritionist':
            return center.hour_nutritionist_price * duration_hours
        elif type == 'trainer':
            return center.hour_trainer_price * duration_hours
        else:
            raise ValidationError('Invalid prenotation type.')
