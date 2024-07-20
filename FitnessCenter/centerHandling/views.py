from django.http import JsonResponse
import json
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .models import ( Employee, Exit, Center, Review)

#<=========================================  Employee  ==========================================================>
class EmployeeView(APIView):
    def get(self, request, uuid=None):
        if uuid:
            employee = get_object_or_404(Employee, uuid=uuid)
            employee_data = {
                "uuid": str(employee.uuid),
                "first_name": employee.first_name,
                "last_name": employee.last_name,
                "DOB": employee.DOB,
                "salary": employee.salary,
                "fiscalCode": employee.fiscalCode,
                "type": employee.type,
                "hiring_date": employee.hiring_date,
                "attachments_uuid": employee.attachments_uuid
            }
            return JsonResponse({"employee": employee_data})
        else:
            employees = Employee.objects.all()
            employees_list = list(employees.values())
            return JsonResponse({"employees": employees_list}, safe=False)

    def post(self, request):
        # Gestione della creazione di un nuovo impiegato
        return JsonResponse({"ok": "nonOk"})

    def put(self, request, uuid):
        employee = get_object_or_404(Employee, uuid=uuid)
        # Aggiorna l'impiegato
        return JsonResponse({"employee": employee})

    def delete(self, request, uuid):
        employee = get_object_or_404(Employee, uuid=uuid)
        employee.delete()
        return JsonResponse({"message": "Employee deleted successfully"})


def show_employee_exits(request, uuid):
    employee = get_object_or_404(Employee, uuid=uuid)
    JsonResponse({"employee":employee})


#<=========================================  Exit  ==========================================================>

class ExitView(APIView):
    def get(self, request, uuid=None):
        if uuid:
            exit = get_object_or_404(Exit, uuid=uuid)
            exit_data = {
                "uuid": str(exit.uuid),
                "amount": exit.amount,
                "type": exit.type,
                "description": exit.description,
                "frequency": exit.frequency,
                "center_uuid": exit.center_uuid,
                "employee_uuid": exit.employee_uuid,
                "start_date": exit.start_date,
                "expiration_date": exit.expiration_date
            }
            return JsonResponse({"exit": exit_data})
        else:
            exits = Exit.objects.all()
            exits_list = list(exits.values())
            return JsonResponse({"exits": exits_list}, safe=False)

    def post(self, request):
        # Gestione della creazione di un nuovo impiegato
        return JsonResponse({"ok": "nonOk"})

    def put(self, request, uuid):
        employee = get_object_or_404(Employee, uuid=uuid)
        # Aggiorna l'impiegato
        return JsonResponse({"employee": employee})

    def delete(self, request, uuid):
        employee = get_object_or_404(Employee, uuid=uuid)
        employee.delete()
        return JsonResponse({"message": "Employee deleted successfully"})




#<=========================================  Center  ==========================================================>


class CenterView(APIView):
    def get(self, request, uuid=None):
        if uuid:
            center = get_object_or_404(Center, uuid=uuid)
            center_data = {
                "uuid": str(center.uuid),
                "amount": center.amount,
                "type": center.type,
                "description": center.description,
                "frequency": center.frequency,
                "center_uuid": center.center_uuid,
                "employee_uuid": center.employee_uuid,
                "start_date": center.start_date,
                "expiration_date": center.expiration_date
            }
            return JsonResponse({"center": center_data})
        else:
            centers = Center.objects.all()
            centers_list = list(centers.values())
            return JsonResponse({"centers": centers_list}, safe=False)

    def post(self, request):
        # Gestione della creazione di un nuovo impiegato
        return JsonResponse({"ok": "nonOk"})

    def put(self, request, uuid):
        employee = get_object_or_404(Employee, uuid=uuid)
        # Aggiorna l'impiegato
        return JsonResponse({"employee": employee})

    def delete(self, request, uuid):
        employee = get_object_or_404(Employee, uuid=uuid)
        employee.delete()
        return JsonResponse({"message": "Employee deleted successfully"})



#<======================================= Review ================================================>

def show_reviews(request, center_uuid):
    return JsonResponse({"message": "List of reviews"})

def add_review(request, center_uuid):
    return JsonResponse({"message": "Persist of a review"})

