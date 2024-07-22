from django.http import JsonResponse
import json
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.core.exceptions import FieldError
from .utils import DateUtils

from .models import ( Employee, Exit, Center, Review)
from .serializers import (EmployeeSerializer, ExitSerializer, CenterSerializer)
from django.db import IntegrityError, DatabaseError, OperationalError
from django.core.exceptions import ValidationError
import uuid
#<=========================================  Employee  ==========================================================>
class EmployeeView(APIView):
    def post_persist_employee(self, employee):
        exit_data = {
            'uuid': uuid.uuid4(),
            'type': 'salary',
            'amount': employee.salary,
            'description': f'salary per month of employee {employee.get_full_name()}',
            'frequency': 1,
            'center_uuid': employee.center_uuid,
            'employee_uuid': employee.uuid,
            'start_date': employee.hiring_date,
            'expiration_date': employee.end_contract_date,
            'is_active': True
        }
        exit_serializer = ExitSerializer(data=exit_data)
        if exit_serializer.is_valid():
            exit_serializer.save()
        else:
            # Handle serializer errors if needed
            print(exit_serializer.errors)        

    
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
        serializer = EmployeeSerializer(data=data)
        if serializer.is_valid():
            employee = serializer.save()
            self.post_persist_employee(employee=employee)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

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

    def get(self, request, uuid=None):
        
        if uuid:
            try:
                employee = get_object_or_404(Employee, uuid=uuid)
                employee_data = EmployeeSerializer(employee).data
                return JsonResponse({"employee": employee_data})
            except ValidationError:
                return JsonResponse({"error": "Invalid UUID format"}, status=400)
        else:

            try:
                employees = self.get_search(request.GET)
                list_size = employees.count()
                start_row = int(request.GET.get('startRow', 0))
                page_size = int(request.GET.get('pageSize', 10))
                if(page_size < 0):
                    raise ValueError("the pageSize cannot be negative.")
                if(start_row < 0):
                    raise ValueError("the startRow cannot be negative.")
                if(start_row > list_size):          #non restituisco nulla ma informo con l'header dei risultati
                    return JsonResponse({"employees": None}, headers={"List-Size": str(list_size)})

                
                paginated_employees = employees[start_row:start_row + page_size]

                # Serializza i dati
                employees_list = EmployeeSerializer(paginated_employees, many=True).data
                
                return JsonResponse({"employees": employees_list}, headers={"List-Size": str(list_size)})
            except ValueError as e:
                return JsonResponse({"error": str(e)}, status=400)
            except FieldError:
                return JsonResponse({"error": "Invalid orderBy parameter"}, status=400)


    def put(self, request, uuid):
        try:
            employee = get_object_or_404(Employee, uuid=uuid)
            data = json.loads(request.body)
        except ValidationError:
                return JsonResponse({"error": "Invalid UUID format"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        if uuid == str(data.get('uuid')):
            serializer = EmployeeSerializer(employee, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=200)
            return JsonResponse(serializer.errors, status=400)
        else:
            return JsonResponse({"error": "uuid must be the same."}, status=400)

    def delete(self, request, uuid):
        try:
            employee = get_object_or_404(Employee, uuid=uuid)
            employee.is_active=False
            employee.save() 
            employee_data = EmployeeSerializer(employee).data
            return JsonResponse({"employee": employee_data}, status=200)
        except ValidationError:
                return JsonResponse({"error": "Invalid UUID format"}, status=400)
        except IntegrityError as e:
            return JsonResponse({"error": "Database integrity error: " + str(e)}, status=400)
        except OperationalError as e:
            return JsonResponse({"error": "Database operational error: " + str(e)}, status=503)
        except DatabaseError as e:
            return JsonResponse({"error": "Database error: " + str(e)}, status=500)
        except Exception as e:
            return JsonResponse({"error": "An unexpected error occurred: " + str(e)}, status=500)




def show_employee_exits(request, uuid):
    try:
        employee = get_object_or_404(Employee, pk=uuid.UUID(uuid))
        exits = Exit.objects.filter(center_uuid=employee.center_uuid, uuid=uuid).all()
        serializer = ExitSerializer(exits, many=True)
        JsonResponse({"exits":serializer.data})
    except ValidationError:
            return JsonResponse({"error": "Invalid UUID format"}, status=400)


#<=========================================  Exit  ==========================================================>

class ExitView(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
        serializer = ExitSerializer(data=data)
        if serializer.is_valid():
            exit = serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    def get_search(self, query_params):
        exits = Exit.objects.all()

        order_by = query_params.get('orderBy', '-start_date')
        if query_params.get('obj.uuid') is not None:
            exits=exits.filter(uuid=query_params.get('obj.uuid'))
        if query_params.get('obj.amount') is not None:
            exits=exits.filter(amount=float(query_params.get('obj.amount')))
        if query_params.get('obj.type') is not None:
            exits=exits.filter(type=query_params.get('obj.type'))
        if query_params.get('like.description') is not None:
            exits=exits.filter(fiscalCode__icontains=query_params.get('like.description'))
        if query_params.get('obj.frequency') is not None:
            exits=exits.filter(frequency=int(query_params.get('obj.frequency')))
        if query_params.get('obj.center_uuid') is not None:
            exits=exits.filter(center_uuid=query_params.get('obj.center_uuid'))
        if query_params.get('obj.exit_uuid') is not None:
            exits=exits.filter(exit_uuid=query_params.get('obj.exit_uuid'))
        if query_params.get('from.start_date') is not None:
            exits=exits.filter(start_date__gte=DateUtils.parse_string_to_date(query_params.get('from.start_date')))
        if query_params.get('to.start_date') is not None:
            exits=exits.filter(start_date__lte=DateUtils.parse_string_to_date(query_params.get('to.start_date')))
        if query_params.get('obj.start_date') is not None:
            exits=exits.filter(start_date=DateUtils.parse_string_to_date(query_params.get('obj.start_date')))
        if query_params.get('from.expiration_date') is not None:
            exits=exits.filter(expiration_date__gte=DateUtils.parse_string_to_date(query_params.get('from.expiration_date')))
        if query_params.get('to.expiration_date') is not None:
            exits=exits.filter(expiration_date__lte=DateUtils.parse_string_to_date(query_params.get('to.expiration_date')))
        if query_params.get('obj.expiration_date') is not None:
            exits=exits.filter(expiration_date=DateUtils.parse_string_to_date(query_params.get('obj.expiration_date')))
    
        if query_params.get('obj.is_active') is not None and query_params.get('obj.is_active').strip().lower() == 'false':
            exits=exits.filter(is_active=False)
        else:
           exits= exits.filter(is_active=True)

        exits = exits.all().order_by(order_by)
        
        return exits



    def get(self, request, uuid=None):
        
        if uuid:
            try:
                exit_istance = get_object_or_404(Exit, uuid=uuid)
                exit_data = ExitSerializer(exit_istance).data
                return JsonResponse({"exit": exit_data})
            except ValidationError:
                return JsonResponse({"error": "Invalid UUID format"}, status=400)
        else:
            try:
                exits = self.get_search(request.GET)
                list_size = exits.count()
                start_row = int(request.GET.get('startRow', 0))
                page_size = int(request.GET.get('pageSize', 10))
                if(page_size < 0):
                    raise ValueError("the pageSize cannot be negative.")
                if(start_row < 0):
                    raise ValueError("the startRow cannot be negative.")
                if(start_row > list_size):          #non restituisco nulla ma informo con l'header dei risultati
                    return JsonResponse({"exits": None}, headers={"List-Size": str(list_size)})

                
                paginated_exits = exits[start_row:start_row + page_size]

                # Serializza i dati
                exits_list = ExitSerializer(paginated_exits, many=True).data
                
                return JsonResponse({"exits": exits_list}, headers={"List-Size": str(list_size)})
            except ValueError as e:
                return JsonResponse({"error": str(e)}, status=400)
            except FieldError:
                return JsonResponse({"error": "Invalid orderBy parameter"}, status=400)


    def put(self, request, uuid):
        try:
            exit_istance = get_object_or_404(Exit, uuid=uuid)
            data = json.loads(request.body)
        except ValidationError:
                return JsonResponse({"error": "Invalid UUID format"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        if uuid == str(data.get('uuid')):
            serializer = ExitSerializer(exit_istance, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=200)
            return JsonResponse(serializer.errors, status=400)
        else:
            return JsonResponse({"error": "uuid must be the same."}, status=400)

    def delete(self, request, uuid):
        try:
            exit_istance = get_object_or_404(Exit, uuid=uuid)
            exit_istance.is_active=False
            exit_istance.save() 
            exit_data = ExitSerializer(exit_istance).data
            return JsonResponse({"exit": exit_data}, status=200)
        except ValidationError:
                return JsonResponse({"error": "Invalid UUID format"}, status=400)
        except IntegrityError as e:
            return JsonResponse({"error": "Database integrity error: " + str(e)}, status=400)
        except OperationalError as e:
            return JsonResponse({"error": "Database operational error: " + str(e)}, status=503)
        except DatabaseError as e:
            return JsonResponse({"error": "Database error: " + str(e)}, status=500)
        except Exception as e:
            return JsonResponse({"error": "An unexpected error occurred: " + str(e)}, status=500)




#<=========================================  Center  ==========================================================>


class CenterView(APIView):
    
    def get_search(self, query_params):
        centers = Center.objects.all()

        order_by = query_params.get('orderBy', 'name')
        if query_params.get('obj.uuid') is not None:
            centers=centers.filter(uuid=query_params.get('obj.uuid'))
        if query_params.get('like.name') is not None:
            centers=centers.filter(name__icontains=query_params.get('like.name'))
        if query_params.get('like.description') is not None:
            centers=centers.filter(description__icontains=query_params.get('like.description'))
        if query_params.get('obj.manager_id') is not None:
            centers=centers.filter(manager_id=query_params.get('obj.manager_id'))
        if query_params.get('obj.province') is not None:
            centers=centers.filter(province=query_params.get('obj.province'))
        if query_params.get('like.city') is not None:
            centers=centers.filter(city__icontains=query_params.get('like.city'))
        if query_params.get('like.street') is not None:
            centers=centers.filter(city__icontains=query_params.get('like.street'))
        if query_params.get('obj.house_number') is not None:
            centers=centers.filter(uuid=int(query_params.get('obj.house_number')))
        if query_params.get('obj.is_active') is not None and query_params.get('obj.is_active').strip().lower() == 'false':
            print("is_active: "+query_params.get('obj.is_active'))
            centers=centers.filter(is_active=False)
        else:
            centers=centers.filter(is_active=True)

        centers = centers.all().order_by(order_by)
        
        return centers  


    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
        serializer = CenterSerializer(data=data)
        if serializer.is_valid():
            center = serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    def get(self, request, uuid=None):
        
        if uuid:
            try:
                center = get_object_or_404(Center, uuid=uuid)
                center_data = CenterSerializer(center).data
                return JsonResponse({"center": center_data})
            except ValidationError:
                return JsonResponse({"error": "Invalid UUID format"}, status=400)
        else:
            try:
                centers = self.get_search(request.GET)
                list_size = centers.count()
                start_row = int(request.GET.get('startRow', 0))
                page_size = int(request.GET.get('pageSize', 10))
                if(page_size < 0):
                    raise ValueError("the pageSize cannot be negative.")
                if(start_row < 0):
                    raise ValueError("the startRow cannot be negative.")
                if(start_row > list_size):          #non restituisco nulla ma informo con l'header dei risultati
                    return JsonResponse({"centers": None}, headers={"List-Size": str(list_size)})

                
                paginated_centers = centers[start_row:start_row + page_size]

                # Serializza i dati
                centers_list = CenterSerializer(paginated_centers, many=True).data
                
                return JsonResponse({"centers": centers_list}, headers={"List-Size": str(list_size)})
            except ValueError as e:
                return JsonResponse({"error": str(e)}, status=400)
            except FieldError:
                return JsonResponse({"error": "Invalid orderBy parameter"}, status=400)


    def put(self, request, uuid):
        try:
            center = get_object_or_404(Center, uuid=uuid)
            data = json.loads(request.body)
        except ValidationError:
                return JsonResponse({"error": "Invalid UUID format"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        if uuid == str(data.get('uuid')):
            serializer = CenterSerializer(center, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=200)
            return JsonResponse(serializer.errors, status=400)
        else:
            return JsonResponse({"error": "uuid must be the same."}, status=400)

    def delete(self, request, uuid):
        try:
            center = get_object_or_404(Center, uuid=uuid)
            center.is_active=False
            center.save() 
            center_data = CenterSerializer(center).data
            return JsonResponse({"center": center_data}, status=200)
        except ValidationError:
                return JsonResponse({"error": "Invalid UUID format"}, status=400)
        except IntegrityError as e:
            return JsonResponse({"error": "Database integrity error: " + str(e)}, status=400)
        except OperationalError as e:
            return JsonResponse({"error": "Database operational error: " + str(e)}, status=503)
        except DatabaseError as e:
            return JsonResponse({"error": "Database error: " + str(e)}, status=500)
        except Exception as e:
            return JsonResponse({"error": "An unexpected error occurred: " + str(e)}, status=500)



#<======================================= Review ================================================>

def show_reviews(request, center_uuid):
    return JsonResponse({"message": "List of reviews"})

def add_review(request, center_uuid):
    return JsonResponse({"message": "Persist of a review"})

