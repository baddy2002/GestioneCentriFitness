
from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from rest_framework import status 
from rest_framework.test import APIClient, APITestCase
from .models import Employee, Exit, Center, Review
import json
import requests

#Tests Structure:

###TestCase gestisce automaticamente la creazione e la pulizia del database per ogni test
###APIClient per simulare richieste HTTP alla tua API
###Verifichiamo che il codice di stato della risposta e il contenuto siano quelli attesi.
###
###



class AuthenticatedAPITestCase(APITestCase):
    client = APIClient()                        #Client a cui tutti i test faranno riferimento che terrà impostato l'header Authentication
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.authenticate()

    @classmethod
    def authenticate(cls):
        url = f"{settings.BACKEND_SSO_SERVICE_PROTOCOL}://{settings.BACKEND_SSO_SERVICE_DOMAIN}:{settings.BACKEND_SSO_SERVICE_PORT}/api/jwt/create"
        credentials = {
            "email": "andreabenassi02@gmail.com",
            "password": "albicocca"
        }
        response = requests.post(url, data=json.dumps(credentials), headers={"Content-Type":"application/json"})
        
        if response.status_code == 200:
            tokens = response.json()
            cls.access_token = tokens['access']
            cls.refresh_token = tokens['refresh']
            cls.client.credentials(HTTP_AUTHORIZATION=f"Bearer {cls.access_token}")             #ogni istanza della classe(ogni classe avrà un proprio token quindi impossibile scada)
        else:
            raise Exception("Authentication failed")

        

class EmployeeAPITestCase(AuthenticatedAPITestCase):
    def setUp(self):
        self.url = reverse('employee-views')
        self.invalid_client = APIClient()

    def test_post_missing_fields(self):                                                 #assicura che non venga persistito se mancano campi
        data = {
            "first_name": "John",
            "last_name": "Doe"
        }
        invalid_response = self.invalid_client.post(self.url, data, format='json')
        self.assertEqual(invalid_response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = AuthenticatedAPITestCase.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('DOB', response_data)
        self.assertIn('salary', response_data)
        self.assertIn('fiscalCode', response_data)
        self.assertIn('type', response_data)
        self.assertIn('hiring_date', response_data)
        self.assertEqual(response_data['DOB'], ['This field is required.'])
        self.assertEqual(response_data['salary'], ['This field is required.'])
        self.assertEqual(response_data['fiscalCode'], ['This field is required.'])
        self.assertEqual(response_data['type'], ['This field is required.'])
        self.assertEqual(response_data['hiring_date'], ['This field is required.'])


    def test_post_invalid_type(self):                                       #assicura che non venga persistito se il tipo non è corretto
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "DOB": "1990-01-01",
            "salary": -400,
            "fiscalCode": "DOEJHN90A01H501",  # Invalid fiscal code
            "center_uuid": "6b016367-8ffd-4e5d-ad96-e16a6c4433f4",
            "user_uuid": "e16a6c44-8ffd-1234-1234-6b016367332o",
            "type": "manager",  # Invalid type
            "hiring_date": "2025-03-01",
            "end_contract_date": "2025-02-01",
            "attachments_uuid": "123e4567-e89b-12d3-a456-426614174000"
        }
        invalid_response = self.invalid_client.post(self.url, data, format='json')
        self.assertEqual(invalid_response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = AuthenticatedAPITestCase.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('type', response_data)
        self.assertIn('fiscalCode', response_data)
        self.assertEqual(response_data['type'], ['"manager" is not a valid choice.'])
        self.assertEqual(response_data['fiscalCode'], ["Fiscal code not valid. It should be long only 16 and contain alphanumeric characters only."])
        self.assertIn('salary', response_data)
        self.assertEqual(response_data['salary'], ["Salary cannot be negative."])

    def test_post_invalid_contract_date(self):                             #assicura che non venga persistito in caso di salario sbagliato
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "DOB": "1990-01-01",
            "salary": -400,
            "center_uuid": "6b016367-8ffd-4e5d-ad96-e16a6c4433f4",
            "fiscalCode": "DOEJHN90A01H501Z",
            "type": "trainer",
            "hiring_date": "2025-03-01",
            "end_contract_date": "2025-02-01",
            "attachments_uuid": "123e4567-e89b-12d3-a456-426614174000"
        }
        invalid_response = self.invalid_client.post(self.url, data, format='json')
        self.assertEqual(invalid_response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = AuthenticatedAPITestCase.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('salary', response_data)
        self.assertEqual(response_data['salary'], ["Salary cannot be negative."])

    def test_post_invalid_employee(self):                           #assicura non venga persistito se il center uuid non esiste
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "DOB": "1990-01-01",
            "salary": -400,
            "center_uuid": "6b016367-8ffd-4e5d-ad96-e16a6c4433f3",      #random 36^32 possibilità sia presente nel db di test
            "user_uuid": "e16a6c44-8ffd-1234-1234-6b016367332o",
            "fiscalCode": "DOEJHN90A01H501Z",
            "type": "trainer",
            "hiring_date": "2025-03-01",
            "end_contract_date": "2025-02-01",
            "attachments_uuid": "123e4567-e89b-12d3-a456-426614174000"
        }
        invalid_response = self.invalid_client.post(self.url, data, format='json')
        self.assertEqual(invalid_response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = AuthenticatedAPITestCase.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('center_uuid', response_data)
        self.assertEqual(response_data['center_uuid'], ["Center with this center_uuid does not exist."])

    def test_post_valid_employee(self):                             #assicura che venga persistito in caso di dati corretti
        center_data = {
            "description": "first test",
            "name": 
                "test",
            "manager_id": 
                "test"
            ,
            "province": 
                "RE"
            ,
            "city": 
                "Viano"
            ,
            "street": 
                "via emilia"
            ,
            "house_number": 
            18
            
        }
        invalid_response = self.invalid_client.post(reverse('center-views'), center_data, format='json')
        self.assertEqual(invalid_response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = AuthenticatedAPITestCase.client.post(reverse('center-views'), center_data, format='json')           #post di un center random per validare il center_uuid
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "DOB": "1990-01-01",
            "salary": 50000,
            "fiscalCode": "DOEJHN90A01H501Z",
            "center_uuid":str(Center.objects.first().uuid),
            "user_uuid": "e16a6c44-8ffd-1234-1234-6b016367332o",
            "type": "trainer",
            "hiring_date": "2025-01-01",
            "end_contract_date": "2025-02-01",
            "attachments_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "is_active": True
        }
        invalid_response = self.invalid_client.post(self.url, data, format='json')
        self.assertEqual(invalid_response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = AuthenticatedAPITestCase.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.get(pk=response.json().get('uuid')).fiscalCode, "DOEJHN90A01H501Z")
        return response

    def test_fetch_incorrect_employee(self):               #controlla che se un uuid non è nel formato corretto restituisca 400, che se non trovato restituisce 404
        response = self.test_post_valid_employee()         #crea un utente(con test case non è assicurato l'ordine dei test)

        # Recupero dell'ID del dipendente creato
        employee_id = response.json().get('uuid')

        # Recupero del dipendente
        fetch_url = self.url+employee_id+"incorrect"
        invalid_response = self.invalid_client.get(fetch_url)
        self.assertEqual(invalid_response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = AuthenticatedAPITestCase.client.get(fetch_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.json())
        self.assertEqual(response.json().get('error'), "Invalid UUID format")

        response = AuthenticatedAPITestCase.client.get(self.url+'57742429-8895-4611-9463-032254433211')  #uuid rando probabilità che esista nel db 36^32
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.json())
        self.assertEqual(response.json().get('detail'), "No Employee matches the given query.")




    def test_fetch_valid_employee(self):
        response = self.test_post_valid_employee()         #crea un utente(con test case non è assicurato l'ordine dei test)

        # Recupero dell'ID del dipendente creato
        employee_id = response.json().get('uuid')

        # Recupero del dipendente
        fetch_url = self.url+employee_id
        invalid_response = self.invalid_client.get(fetch_url)
        self.assertEqual(invalid_response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = AuthenticatedAPITestCase.client.get(fetch_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



    def test_update_invalid_employee(self):
        response = self.test_post_valid_employee()         #crea un utente(con test case non è assicurato l'ordine dei test)
        uuid =response.json().get("uuid")
        updated_data = {
            "uuid": uuid+"incorrect",
            "first_name": "John",
            "last_name": "Doe",
            "DOB": "1990-01-01",
            "salary": 50000,
            "fiscalCode": "DOEJHN90A01H501Z",
            "center_uuid": "6b016367-8ffd-4e5d-ad96-e16a6c4433f4",
            "type": "trainer",
            "hiring_date": "2022-01-01",
            "attachments_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "is_active": True
        }
        update_url=self.url+uuid
        invalid_response = self.invalid_client.put(update_url, updated_data, format='json')
        self.assertEqual(invalid_response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = AuthenticatedAPITestCase.client.put(update_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], "uuid must be the same.")


    def test_update_valid_employee(self):
        response = self.test_post_valid_employee()         #crea un utente(con test case non è assicurato l'ordine dei test)
        uuid =response.json().get("uuid")
        updated_data = {
            "uuid": response.json().get("uuid"),
            "first_name": "John",
            "last_name": "Doe",
            "DOB": "1990-01-01",
            "salary": 50000,
            "fiscalCode": "DOEJHN90A01H501Z",
            "type": "trainer",
            "hiring_date": "2022-01-01",
            "attachments_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "is_active": True
        }
        update_url=self.url+uuid
        invalid_response = self.invalid_client.put(update_url, updated_data, format='json')
        self.assertEqual(invalid_response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = AuthenticatedAPITestCase.client.put(update_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        fetched_data = response.json()
        self.assertEqual(fetched_data['uuid'], updated_data.get("uuid"))
        self.assertEqual(fetched_data['first_name'], updated_data.get("first_name"))
        self.assertEqual(fetched_data['last_name'], updated_data.get("last_name"))
        self.assertEqual(fetched_data['DOB'], updated_data.get("DOB"))
        self.assertEqual(fetched_data['salary'], "50000.00")
        self.assertEqual(fetched_data['fiscalCode'], updated_data.get("fiscalCode"))
        self.assertEqual(fetched_data['type'], updated_data.get("type"))
        self.assertEqual(fetched_data['hiring_date'], updated_data.get("hiring_date"))
        self.assertEqual(fetched_data['attachments_uuid'], updated_data.get("attachments_uuid"))
        self.assertEqual(fetched_data['is_active'], updated_data.get('is_active'))


    def test_delete_employee(self):                         #controlla che un utente con id corretto venga disattiva, controlla che gli errori siano consoni

        response = self.test_post_valid_employee()         #crea un utente(con test case non è assicurato l'ordine dei test)
        uuid = response.json().get('uuid')
        delete_url=self.url+uuid+"incorrect"
        invalid_response = self.invalid_client.delete(delete_url)
        self.assertEqual(invalid_response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = AuthenticatedAPITestCase.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = AuthenticatedAPITestCase.client.get(self.url+'57742429-8895-4611-9463-032254433211')  #uuid rando probabilità che esista nel db 36^32
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.json())
        self.assertEqual(response.json().get('detail'), "No Employee matches the given query.")

        delete_url=self.url+uuid
        response = AuthenticatedAPITestCase.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertIn('employee', response_data)
        self.assertEqual(response_data['employee'].get('is_active'), False)
        
        # Verifica che il dipendente sia stato contrassegnato come inattivo
        employee = Employee.objects.get(uuid=uuid)
        self.assertFalse(employee.is_active)
        
#<===================================== EXIT ====================================================>

class ExitAPITestCase(AuthenticatedAPITestCase):
    def setUp(self):
        self.url = reverse('exit-views')
        self.invalid_client = APIClient()

    def test_post_missing_fields(self):                          #assicura che non venga persistito se mancano campi
        data = {
            "amount": 10,
            "type": "salary",
            "description": "salary_wrong_test"
        }
        
        response = AuthenticatedAPITestCase.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('center_uuid', response_data)
        self.assertIn('start_date', response_data)
        self.assertEqual(response_data['center_uuid'], ['This field is required.'])
        self.assertEqual(response_data['start_date'], ['This field is required.'])


    def test_post_invalid_type_amount_frequency_centeruuid_expiration(self):       #assicura che non venga persistito uno dei campi nel titolo non è corretto
        data = {
            "amount": -10,
            "type": "wrongType",
            "frequency": -1,
            "description": "salary_wrong_test",
            "center_uuid": "6b016367-8ffd-4e5d-ad96-e16a6c4433f3",
            "start_date": "2024-03-11",
            "expiration_date": "2022-03-03"
        }
        response = AuthenticatedAPITestCase.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('amount', response_data)
        self.assertIn('type', response_data)
        self.assertIn('frequency', response_data)
        self.assertIn('center_uuid', response_data)
        self.assertIn('expiration_date', response_data)
        self.assertEqual(response_data['amount'], ['Amount cannot be negative.'])
        self.assertEqual(response_data['type'], ['\"wrongType\" is not a valid choice.'])
        self.assertEqual(response_data['frequency'], ['Frequency cannot be negative.'])
        self.assertEqual(response_data['center_uuid'], ['Center with this center_uuid does not exist.'])
        self.assertEqual(response_data['expiration_date'], ['Expiration date cannot be in the past.'])

    def test_post_invalid_frequency_employuuid(self):                          #assicura non venga persistito se il tipo è salary 
        employee_test = EmployeeAPITestCase()
        employee_test.setUp()
        
        employee_test.test_post_valid_employee()                          #creo un employee(con un centro associato)
        
        data = {
                "amount": 10,
                "type": "salary",
                "frequency": 2,
                "description": "salary_wrong_test",
                "center_uuid":  str(Center.objects.first().uuid),              #un center esistente
                "start_date": "2024-03-11",
                "expiration_date": "2025-03-03",
                "employee_uuid": str(Employee.objects.first().uuid)               #un employee esistente
            }
        response = AuthenticatedAPITestCase.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('non_field_errors', response_data)
        self.assertEqual(response_data['non_field_errors'], ["The salary's frequency should be once per month."])
        data = {
            "amount": 10,
            "type": "salary",
            "frequency": 1,
            "description": "salary_wrong_test",
            "center_uuid":  str(Center.objects.first().uuid),              #un center esistente
            "start_date": "2024-03-11",
            "expiration_date": "2025-03-03"
        }                                                          #employee non presente(o sbagliato)
        response = AuthenticatedAPITestCase.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('non_field_errors', response_data)
        self.assertEqual(response_data['non_field_errors'], ["Employee with this employee_uuid does not exist."])


    def test_post_valid_exit(self):                             #assicura che venga persistito in caso di dati corretti
        employee_test = EmployeeAPITestCase()
        employee_test.setUp()
        employee_test.test_post_valid_employee()                          #creo un employee(con un centro associato)
        
        data = {
            "amount": 10,
            "type": "salary",
            "frequency": 1,
            "description": "correct_test",
            "center_uuid": str(Center.objects.first().uuid),
            "start_date": "2024-03-11",
            "expiration_date": "2025-03-03",
            "employee_uuid":  str(Employee.objects.first().uuid)
        }
        invalid_response = self.invalid_client.post(self.url, data, format='json')
        self.assertEqual(invalid_response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = AuthenticatedAPITestCase.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        exit_data = Exit.objects.get(pk=response.json().get('uuid'))
        self.assertEqual(exit_data.employee_uuid, data.get('employee_uuid'))
        self.assertEqual(exit_data.expiration_date.strftime('%Y-%m-%d'), data.get('expiration_date'))
        self.assertEqual(exit_data.start_date.strftime('%Y-%m-%d'), data.get('start_date'))
        self.assertEqual(exit_data.center_uuid, data.get('center_uuid'))
        self.assertEqual(exit_data.description, data.get('description'))
        self.assertEqual(exit_data.frequency, data.get('frequency'))
        self.assertEqual(exit_data.type, data.get('type'))
        self.assertEqual(exit_data.amount, data.get('amount'))
        return response

    def test_fetch_incorrect_exit(self):               #controlla che se un uuid non è nel formato corretto restituisca 400, che se non trovato restituisce 404
        response = self.test_post_valid_exit()         #crea un' uscita(con test case non è assicurato l'ordine dei test)


        exit_id = response.json().get('uuid')
        fetch_url = self.url+exit_id+"incorrect"

        response = AuthenticatedAPITestCase.client.get(fetch_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.json())
        self.assertEqual(response.json().get('error'), "Invalid UUID format")

        response = AuthenticatedAPITestCase.client.get(self.url+'57742429-8895-4611-9463-032254433211')  #uuid rando probabilità che esista nel db 36^32
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.json())
        self.assertEqual(response.json().get('detail'), "No Exit matches the given query.")


    def test_fetch_valid_exit(self):
        response = self.test_post_valid_exit()         #crea un utente(con test case non è assicurato l'ordine dei test)

        exit_id = response.json().get('uuid')
        fetch_url = self.url+exit_id
        invalid_response = self.invalid_client.get(fetch_url)
        self.assertEqual(invalid_response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = AuthenticatedAPITestCase.client.get(fetch_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json().get('exit')
        exit_data = Exit.objects.filter(pk=exit_id).get()
        
        self.assertEqual(str(exit_data.uuid), response_data.get('uuid'))
        self.assertEqual(str(exit_data.amount), response_data.get("amount"))
        self.assertEqual(exit_data.type, response_data.get("type"))
        self.assertEqual(exit_data.frequency, response_data.get("frequency"))
        self.assertEqual(exit_data.description, response_data.get('description'))
        self.assertEqual(exit_data.center_uuid, response_data.get("center_uuid"))
        self.assertEqual(exit_data.start_date.strftime('%Y-%m-%d'), response_data.get("start_date"))
        self.assertEqual(exit_data.expiration_date.strftime('%Y-%m-%d'), response_data.get("expiration_date"))
        self.assertEqual(exit_data.employee_uuid, response_data.get("employee_uuid"))
        self.assertEqual(exit_data.is_active, response_data.get('is_active'))



    def test_update_invalid_exit(self):
        response = self.test_post_valid_exit()         #crea un utente(con test case non è assicurato l'ordine dei test)
        uuid =response.json().get("uuid")
        updated_data = {
            "uuid": uuid+"incorrect",
            "amount": 9,
            "type": "salary",
            "frequency": 1,
            "description": "salary_wrong_test",
            "center_uuid": "6b016367-8ffd-4e5d-ad96-e16a6c4433f4",
            "start_date": "2024-03-11",
            "expiration_date": "2025-03-03",
            "employee_uuid": "8fec1694-eba2-464f-bdf1-28f269853cfe"
        }
        update_url=self.url+uuid
        response = AuthenticatedAPITestCase.client.put(update_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], "uuid must be the same.")


    def test_update_valid_exit(self):
        response = self.test_post_valid_exit()         #crea un utente(con test case non è assicurato l'ordine dei test)
        uuid =response.json().get("uuid")
        updated_data = {
            "uuid": response.json().get("uuid"),
            "amount": 10,
            "type": "salary",
            "frequency": 1,
            "description": "salary_wrong_test",
            "center_uuid": str(Center.objects.first().uuid),
            "start_date": "2024-03-11",
            "expiration_date": "2025-03-03",
            "employee_uuid": str(Employee.objects.first().uuid)
        }
        update_url=self.url+uuid
        invalid_response = self.invalid_client.get(update_url, updated_data, format='json')
        self.assertEqual(invalid_response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = AuthenticatedAPITestCase.client.put(update_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        fetched_data = response.json()
        self.assertEqual(fetched_data['uuid'], updated_data.get('uuid'))
        self.assertEqual(fetched_data['amount'], f"{float(updated_data.get('amount')):.2f}")
        self.assertEqual(fetched_data['type'], updated_data.get("type"))
        self.assertEqual(fetched_data['frequency'], updated_data.get("frequency"))
        self.assertEqual(fetched_data['description'], updated_data.get("description"))
        self.assertEqual(fetched_data['center_uuid'], updated_data.get("center_uuid"))
        self.assertEqual(fetched_data['start_date'], updated_data.get("start_date"))
        self.assertEqual(fetched_data['expiration_date'], updated_data.get("expiration_date"))
        self.assertEqual(fetched_data['employee_uuid'], updated_data.get("employee_uuid"))
        self.assertEqual(fetched_data['is_active'], True if updated_data.get('is_active') is None else False )


    def test_delete_exit(self):                         #controlla che un utente con id corretto venga disattiva, controlla che gli errori siano consoni

        response = self.test_post_valid_exit()         #crea un utente(con test case non è assicurato l'ordine dei test)
        uuid = response.json().get('uuid')
        delete_url=self.url+uuid+"incorrect"
        invalid_response = self.invalid_client.get(delete_url)
        self.assertEqual(invalid_response.status_code, status.HTTP_401_UNAUTHORIZED)       
        response = AuthenticatedAPITestCase.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = AuthenticatedAPITestCase.client.get(self.url+'57742429-8895-4611-9463-032254433211')  #uuid rando probabilità che esista nel db 36^32
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.json())
        self.assertEqual(response.json().get('detail'), "No Exit matches the given query.")

        delete_url=self.url+uuid
        response = AuthenticatedAPITestCase.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertIn('exit', response_data)
        self.assertEqual(response_data['exit'].get('is_active'), False)
        
        # Verifica che il dipendente sia stato contrassegnato come inattivo
        exit_data = Exit.objects.get(uuid=uuid)
        self.assertFalse(exit_data.is_active)

#<===================================== CENTER ====================================================>

class CenterAPITestCase(AuthenticatedAPITestCase):
    def setUp(self):
        self.url = reverse('center-views')
        self.invalid_client = APIClient()

    def test_post_missing_fields(self):                                                 #assicura che non venga persistito se mancano campi
        data = {
            "description": "John",
            "province": "Doe"
        }
        response = AuthenticatedAPITestCase.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('name', response_data)
        self.assertIn('manager_id', response_data)
        self.assertIn('city', response_data)
        self.assertIn('street', response_data)
        self.assertIn('house_number', response_data)
        self.assertEqual(response_data['name'], ['This field is required.'])
        self.assertEqual(response_data['manager_id'], ['This field is required.'])
        self.assertEqual(response_data['city'], ['This field is required.'])
        self.assertEqual(response_data['street'], ['This field is required.'])
        self.assertEqual(response_data['house_number'], ['This field is required.'])


    def test_post_invalid_province_and_house(self):         #assicura che non venga persistito se la provincia non è nel formato corretto
                                                            # e se il numero civico non è un intero positivo
        data = {
            "description": "John",
            "province": "Doe",
            "name": "test",
            "manager_id": "test",
            "province": "test",
            "city": "test",
            "street": "test",
            "house_number": "test"
            
        }
        response = AuthenticatedAPITestCase.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('province', response_data)
        self.assertIn('house_number', response_data)
        self.assertEqual(response_data['province'], ['Ensure this field has no more than 2 characters.'])
        self.assertEqual(response_data['house_number'], ['A valid integer is required.'])


    def test_post_valid_center_and_not_replicate(self):                 #assicura che venga persistito in caso di dati corretti,
                                                                        #assicura che non venga persistito se la provincia, la città, la strada
                                                                        # e il numero civico appartengono già ad un altro centro
        data = {
            "description": "John",
            "name": "test",
            "manager_id": "test",
            "province": "RE",
            "city": "Viano",
            "street": "Via Roma",
            "house_number": 1
        }
        invalid_response = self.invalid_client.post(self.url, data, format='json')
        self.assertEqual(invalid_response.status_code, status.HTTP_401_UNAUTHORIZED)   
        response = AuthenticatedAPITestCase.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Center.objects.get(pk=response.json().get('uuid')).manager_id, "test")
        response2 = AuthenticatedAPITestCase.client.post(self.url, data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response2.json()
        self.assertIn('non_field_errors', response_data)
        self.assertEqual(response_data['non_field_errors'], ['There is another center in this location ! '])
        return response
    

    def test_fetch_incorrect_center(self):               #controlla che se un uuid non è nel formato corretto restituisca 400, che se non trovato restituisce 404
        response = self.test_post_valid_center_and_not_replicate()         #crea un utente(con test case non è assicurato l'ordine dei test)

        # Recupero dell'ID del center creato
        center_id = response.json().get('uuid')

        # Recupero del center
        fetch_url = self.url+center_id+"incorrect"

        response = AuthenticatedAPITestCase.client.get(fetch_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.json())
        self.assertEqual(response.json().get('error'), "Invalid UUID format")

        response = AuthenticatedAPITestCase.client.get(self.url+'57742429-8895-4611-9463-032254433211')  #uuid rando probabilità che esista nel db 36^32
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.json())
        self.assertEqual(response.json().get('detail'), "No Center matches the given query.")




    def test_fetch_valid_center(self):
        response = self.test_post_valid_center_and_not_replicate()         #crea un utente(con test case non è assicurato l'ordine dei test)

        # Recupero dell'ID del dipendente creato
        center_id = response.json().get('uuid')

        # Recupero del dipendente
        fetch_url = self.url+center_id
        response = self.invalid_client.get(fetch_url)               #un customer può vedere un centro 
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invalid_center(self):
        response = self.test_post_valid_center_and_not_replicate()         #crea un utente(con test case non è assicurato l'ordine dei test)
        uuid =response.json().get("uuid")
        updated_data = {
            "uuid": uuid+"incorrect",
            "description": "John",
            "name": "test_2",
            "manager_id": "test_2",
            "province": "MO",
            "city": "Nonantola",
            "street": "Via Saba Umberto",
            "house_number": 26
        }
        update_url=self.url+uuid
        response = AuthenticatedAPITestCase.client.put(update_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], "uuid must be the same.")


    def test_update_valid_center(self):
        response = self.test_post_valid_center_and_not_replicate()         #crea un utente(con test case non è assicurato l'ordine dei test)
        uuid =response.json().get("uuid")
        updated_data = {
            "uuid": uuid,
            "description": "John",
            "name": "test_2",
            "manager_id": "test_2",
            "province": "MO",
            "city": "Nonantola",
            "street": "Via Saba Umberto",
            "house_number": 26
        }
        update_url=self.url+uuid
        invalid_response = self.invalid_client.post(update_url, updated_data, format='json')
        self.assertEqual(invalid_response.status_code, status.HTTP_401_UNAUTHORIZED) 
        response = AuthenticatedAPITestCase.client.put(update_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        fetched_data = response.json()
        self.assertEqual(fetched_data['uuid'], updated_data.get("uuid"))
        self.assertEqual(fetched_data['description'], updated_data.get("description"))
        self.assertEqual(fetched_data['name'], updated_data.get("name"))
        self.assertEqual(fetched_data['manager_id'], updated_data.get("manager_id"))
        self.assertEqual(fetched_data['province'], updated_data.get("province"))
        self.assertEqual(fetched_data['city'], updated_data.get("city"))
        self.assertEqual(fetched_data['street'], updated_data.get("street"))
        self.assertEqual(fetched_data['house_number'], updated_data.get("house_number"))


    def test_delete_center(self):                         #controlla che un utente con id corretto venga disattivato, controlla che gli errori siano consoni

        response = self.test_post_valid_center_and_not_replicate()         #crea un utente(con test case non è assicurato l'ordine dei test)
        uuid = response.json().get('uuid')
        delete_url=self.url+uuid+"incorrect"
        invalid_response = self.invalid_client.delete(delete_url)
        self.assertEqual(invalid_response.status_code, status.HTTP_401_UNAUTHORIZED)         
        response = AuthenticatedAPITestCase.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = AuthenticatedAPITestCase.client.get(self.url+'57742429-8895-4611-9463-032254433211')  #uuid rando probabilità che esista nel db 36^32
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.json())
        self.assertEqual(response.json().get('detail'), "No Center matches the given query.")

        delete_url=self.url+uuid
        response = AuthenticatedAPITestCase.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertIn('center', response_data)
        self.assertEqual(response_data['center'].get('is_active'), False)
        
        # Verifica che il dipendente sia stato contrassegnato come inattivo
        center = Center.objects.get(uuid=uuid)
        self.assertFalse(center.is_active)

