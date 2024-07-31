from django.db import models
import uuid
class Employee(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    TRAINER = 'trainer'
    NUTRITIONIST = 'nutritionist'
    MIXED = "mixed"
    
    EMPLOYEE_TYPE_CHOICES = [
        (TRAINER, 'trainer'),
        (NUTRITIONIST, 'nutritionist'),
        (MIXED, 'mixed')
    ]
    

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    DOB = models.DateField('Date of Birth')
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    fiscalCode = models.CharField(max_length=16)
    email = models.CharField(max_length=255)
    type = models.CharField(
        max_length=50,
        choices=EMPLOYEE_TYPE_CHOICES,
    )
    hiring_date = models.DateField('Hiring Date')
    end_contract_date = models.DateField('End Contract Date', null=True)
    attachments_uuid = models.CharField(max_length=36, blank=True, null=True)
    center_uuid = models.CharField()
    is_active = models.BooleanField(default=False, null=False)


    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return (f"Employee: {self.get_full_name()}, "
                f"DOB: {self.DOB}, "
                f"Salary: {self.salary}, "
                f"Fiscal Code: {self.fiscalCode}, "
                f"Type: {self.type}, "
                f"Hiring Date: {self.hiring_date}, "
                f"Attachments UUID: {self.attachments_uuid}")


class Exit(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    SALARY =  'salary'
    TAX =  'tax'
    SINGLE_EXPENSE = 'single'


    EXIT_TYPE_CHOICES = [
        (SALARY, 'salary'),
        (TAX, 'tax'),
        (SINGLE_EXPENSE, 'single')
    ]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(
        max_length=50,
        choices=EXIT_TYPE_CHOICES,
    )
    description = models.TextField(blank=True,null=True)
    frequency = models.IntegerField(help_text="Frequency in months", null=True)
    center_uuid = models.CharField(max_length=36)
    employee_uuid = models.CharField(max_length=36, null=True)
    start_date = models.DateField('Start Date')
    expiration_date = models.DateField('Expiration Date', null=True)
    is_active = models.BooleanField(default=True, null=False)
    def __str__(self):
        return (f"Exit: Amount: {self.amount}, "
                f"Type: {self.type}, "
                f"Description: {self.description}, "
                f"Frequency: {self.frequency} months, "
                f"Center UUID: {self.center_uuid}, "
                f"Employee UUID: {self.employee_uuid}, "
                f"Start Date: {self.start_date}, "
                f"Expired Date: {self.expired_date()}")


class Center(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    name = models.CharField(max_length=100)
    description = models.TextField()
    manager_id = models.CharField()
    province = models.CharField(max_length=2)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house_number = models.PositiveIntegerField()
    hour_nutritionist_price = models.DecimalField(max_digits=10, decimal_places=2)
    hour_trainer_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True, null=False)

    def __str__(self):
        return (f"Center: {self.name}, "
                f"Description: {self.description}, "
                f"Manager ID: {self.manager_id}, "
                f"Province: {self.province}, "
                f"City: {self.city}, "
                f"Street: {self.street}, "
                f"House Number: {self.house_number}")

class Review(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Score da 1 a 5
    user_id = models.CharField()
    center_uuid = models.CharField(max_length=255)
    exec_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, null=False)


    def __str__(self):
        return (f"Review: Text: {self.text[:50]}..., "  # Mostra solo i primi 50 caratteri del testo
                f"Score: {self.score}, "
                f"User ID: {self.user_id}, "
                f"Center UUID: {self.center_uuid}, "
                f"Execution Time: {self.exec_time}")
    
    def from_map(self, map):
        self.uuid = map.get('uuid')
        self.text = map.get('text')
        self.score = None if map.get('score') is None else int(map.get('score'))


class Prenotation(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=255)
    user_email = models.EmailField(max_length=255)
    employee_uuid = models.CharField(max_length=255)
    center_uuid = models.CharField(max_length=255)
    exec_time = models.DateTimeField(auto_now_add=True)
    from_hour =  models.DateTimeField()
    to_hour =  models.DateTimeField()
    total =  models.DecimalField(max_digits=10, decimal_places=2)
    TYPES_CHOISES = [
        ('trainer', 'trainer'),
        ('nutritionist', 'nutritionist'),
    ]
    type = models.CharField(max_length=16, choices=TYPES_CHOISES, null=False)
    STATUS_CHOICES = [
        ('pending', 'pending'),
        ('confirmed', 'confirmed'),
        ('rejected', 'rejected'),
        ('to cancel', 'to cancel'),
        ('cancelled', 'cancelled'),
        ('completed', 'completed'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

class EmployeeBusyTrace(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)   
    employee_uuid = models.CharField(max_length=255)
    prenotation_hours = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    date = models.DateField(auto_now_add=True)