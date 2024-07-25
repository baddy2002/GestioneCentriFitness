from os import getenv
from django.http import JsonResponse
import json
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.core.exceptions import FieldError
from .utils import DateUtils
from .services import EmployeeService
from .models import ( Employee, Exit, Center, Review)
from .serializers import (EmployeeSerializer, ExitSerializer, CenterSerializer, ReviewSerializer)
from django.db import IntegrityError, DatabaseError, OperationalError
from django.core.exceptions import ValidationError
import jwt
import requests

from .tokenService import get_principal, jwt_base_authetication, jwt_manager_authetication, jwt_nutritionist_authetication, jwt_trainer_authetication
#<=========================================  Employee  ==========================================================>
class EmployeeView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.employee_service = EmployeeService() 
   
    @jwt_manager_authetication
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
        serializer = EmployeeSerializer(data=data)
        if serializer.is_valid():
            employee = serializer.save()
            self.employee_service.post_persist_employee(employee=employee)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    @jwt_manager_authetication
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
                employees = self.employee_service.get_search(request.GET)
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

    @jwt_manager_authetication
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

    @jwt_manager_authetication
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
    @jwt_manager_authetication
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


    @jwt_manager_authetication
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

    @jwt_manager_authetication
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

    @jwt_manager_authetication
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
            centers=centers.filter(is_active=False)
        else:
            centers=centers.filter(is_active=True)

        centers = centers.all().order_by(order_by)
        
        return centers  

    @jwt_manager_authetication
    def post(self, request):
        try:
            data = json.loads(request.body)
            data['manager_id'] = get_principal(request)
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

    @jwt_manager_authetication
    def put(self, request, uuid):
        try:
            center = get_object_or_404(Center, uuid=uuid)
            data = json.loads(request.body)

        except ValidationError:
                return JsonResponse({"error": "Invalid UUID format"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        if uuid == str(data.get('uuid')):
            user_uuid = get_principal(request)
            if center.manager_id != user_uuid:
                return JsonResponse({"error": "Forbidden: the manager that are trying to update the center is not the true manager"}, status=403)
            data['manager_id'] = user_uuid  
            serializer = CenterSerializer(center, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=200)
            return JsonResponse(serializer.errors, status=400)
        else:
            return JsonResponse({"error": "uuid must be the same."}, status=400)

    @jwt_manager_authetication
    def delete(self, request, uuid):
        try:
            center = get_object_or_404(Center, uuid=uuid)
            user_uuid = get_principal(request)
            if center.manager_id != user_uuid:
                return JsonResponse({"error": "Forbidden: the manager that are trying to delete the center is not the true manager"}, status=403)
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
class ReviewView(APIView):
    def get_search(self, query_params):
        reviews = Review.objects.all()

        order_by = query_params.get('orderBy', '-exec_time')
        if query_params.get('obj.uuid') is not None:
            reviews=reviews.filter(uuid=query_params.get('obj.uuid'))
        if query_params.get('like.text') is not None:
            reviews=reviews.filter(text__icontains=query_params.get('like.text'))
        if query_params.get('obj.score') is not None:
            reviews=reviews.filter(score=int(query_params.get('obj.score')))
        if query_params.get('obj.user_id') is not None:
            reviews=reviews.filter(user_id=query_params.get('obj.user_id'))
        if query_params.get('obj.center_uuid') is not None:
            reviews=reviews.filter(center_uuid=query_params.get('obj.center_uuid'))
        if query_params.get('from.exec_time') is not None:
            reviews=reviews.filter(start_date__gte=DateUtils.parse_string_to_datetime(query_params.get('from.exec_time')))
        if query_params.get('to.exec_time') is not None:
            reviews=reviews.filter(start_date__lte=DateUtils.parse_string_to_datetime(query_params.get('to.exec_time')))
        if query_params.get('obj.exec_time') is not None:
            reviews=reviews.filter(start_date=DateUtils.parse_string_to_datetime(query_params.get('obj.exec_time')))
        if query_params.get('obj.is_active') is not None and query_params.get('obj.is_active').strip().lower() == 'false':
            reviews=reviews.filter(is_active=False)
        else:
            reviews=reviews.filter(is_active=True)

        reviews = reviews.all().order_by(order_by)
        
        return reviews 

    def get(self, request, center_uuid):
        try:
            reviews = self.get_search(request.GET)
            list_size = reviews.count()
            start_row = int(request.GET.get('startRow', 0))
            page_size = int(request.GET.get('pageSize', 10))
            if(page_size < 0):
                raise ValueError("the pageSize cannot be negative.")
            if(start_row < 0):
                raise ValueError("the startRow cannot be negative.")
            if(start_row > list_size):          #non restituisco nulla ma informo con l'header dei risultati
                return JsonResponse({"reviews": None}, headers={"listSize": str(list_size)})

            
            paginated_reviews = reviews[start_row:start_row + page_size]

            # Serializza i dati
            reviews_list = ReviewSerializer(paginated_reviews, many=True).data
            
            return JsonResponse({"reviews": reviews_list}, headers={"listSize": str(list_size)})
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except FieldError:
            return JsonResponse({"error": "Invalid orderBy parameter"}, status=400)

    @jwt_base_authetication
    def post(self, request, center_uuid):
        try:
            data = json.loads(request.body)
            data['user_id'] = get_principal(request)
            data['center_uuid'] = center_uuid
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            # TODO: implementare controllo per capire se l'utente ha prenotato
            review = serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    @jwt_base_authetication
    def put(self, request, center_uuid, uuid):
        try:
            review = get_object_or_404(Review, uuid=uuid)
            user_uuid=get_principal(request)
            if review.user_id != user_uuid:          
                return JsonResponse({"error": "Forbidden: the user that modified the review is not the author"}, status=403)
            data = json.loads(request.body)
        except ValidationError:
                return JsonResponse({"error": "Invalid UUID format"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        if uuid == str(data.get('uuid')):
            serializer = ReviewSerializer(review, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=200)
            return JsonResponse(serializer.errors, status=400)
        else:
            return JsonResponse({"error": "uuid must be the same."}, status=400)