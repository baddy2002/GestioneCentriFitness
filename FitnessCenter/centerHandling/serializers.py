# serializers.py
from rest_framework import serializers
from .models import Employee, Exit, Center, Review
import re
from django.utils import timezone
import requests

class EmployeeSerializer(serializers.ModelSerializer):
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
            if self.instance is None:                                       #è una post 
                raise serializers.ValidationError("There is another center in this location ! ")
            else:    
                if center.uuid != uuid:                                        #è una put in cui modifico il luogo e provo a metterlo in uno in cui un negozio esiste già
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