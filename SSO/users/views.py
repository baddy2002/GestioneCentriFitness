from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from djoser.social.views import ProviderAuthView
from django.core.exceptions import FieldError, ValidationError
import jwt
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from django.shortcuts import get_object_or_404
from os import getenv
from .models import UserAccount, Photo, Invito
from .authentication import CustomTokenObtainPairSerializer
import requests
import json
from django.contrib.auth.models import Group
from django.http import JsonResponse
from .serializers import InvitationSerializer, UserAccountSerializer
from .utils import DateUtils, generate_unique_filename, get_principal, registerUser, validate_partita_iva
import base64
from rest_framework.permissions import AllowAny

class CustomProviderAuthView(ProviderAuthView):
    def post(self, request, *args, **kwargs):

        response = super().post(request, *args, **kwargs)

        if response.status_code == 201:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                domain=settings.BACKEND_SERVICE_DOMAIN,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
            response.set_cookie(
                'refresh',
                refresh_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                domain=settings.BACKEND_SERVICE_DOMAIN,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
        user_id = jwt.decode(access_token, getenv('DJANGO_SECRET_KEY'), algorithms=['HS256']).get('user_id')
        user = UserAccount.objects.get(pk=user_id)
        user.is_active = True
        user.save()
        return response


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                domain=settings.BACKEND_SERVICE_DOMAIN,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
            response.set_cookie(
                'refresh',
                refresh_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                domain=settings.BACKEND_SERVICE_DOMAIN,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh')

        if refresh_token:
            request.data['refresh'] = refresh_token

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get('access')

            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                domain=settings.BACKEND_SERVICE_DOMAIN,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE

            )

        return response


class CustomTokenVerifyView(TokenVerifyView): 
    def post(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access')

        if access_token:
            request.data['token'] = access_token

        return super().post(request, *args, **kwargs)

class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)

        response.delete_cookie('access')
        response.delete_cookie('refresh')

        return response
    

def get_direct_url(photo):
    if(photo!=None and photo.filedata!=None):
                    photo_url = photo.filedata.storage.url(photo.filedata.name)
                    direct_url = 'https://drive.google.com/thumbnail?'+photo_url[
                        photo_url.find('id=')                                                       #starindex
                        :photo_url.find('&', photo_url.find('id='))]        #end_index(la prima & dopo startIndex)
                    return direct_url
    return None
class CompleteUserView(APIView):
    parser_classes = [MultiPartParser, FormParser, FileUploadParser]
    def get(self, request, *args, **kwargs):
        url = f'{settings.BACKEND_SERVICE_PROTOCOL}://{settings.BACKEND_SERVICE_DOMAIN}:{settings.BACKEND_SERVICE_PORT}/api/users/me/' 
        headers = {
            'Authorization': f'Bearer {request.COOKIES.get("access")}'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            user = get_object_or_404(UserAccount, pk=json.loads(response.content.decode('utf-8')).get('id'))
            photo = Photo.objects.filter(filename=user.photo).first()
            photo_url=None
            direct_url=get_direct_url(photo)
                               
                    
            json_mapper = {
                'id': str(user.pk),
                'email': str(user.email),
                'first_name': str(user.first_name),
                'last_name': str(user.last_name),
                'data_iscrizione': str(user.data_iscrizione),
                'photo': direct_url if direct_url is not None else None,
                'group': [group.name for group in user.groups.all()]
            }
            return JsonResponse(json_mapper)
        else:
            return JsonResponse({"Error": "Impossible show the data of the user"})
        
    def put(self, request, *args, **kwargs):
        print(request.FILES)
        url = f'{settings.BACKEND_SERVICE_PROTOCOL}://{settings.BACKEND_SERVICE_DOMAIN}:{settings.BACKEND_SERVICE_PORT}/api/users/me/' 
        headers = {
            'Authorization': f'Bearer {request.COOKIES.get("access")}'
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            user = get_object_or_404(UserAccount, pk=json.loads(response.content.decode('utf-8')).get('id'))
            photo = request.FILES.get('photo')

            try:
                if 'id' not in request.data or request.data['id'] is None:
                    raise Exception("ID cannot be null")
                if 'email' not in request.data or request.data['email'] is None:
                    raise Exception("email cannot be null")
                if request.data['id'] != str(user.pk):
                    raise Exception("cannot modify another user! ")
                if request.data['email'] != user.email:
                    raise Exception("You cannot modify the email for the moment")
                

                serializer = UserAccountSerializer(user, data=request.data, partial=True)
                
                if photo:
                    # Salva la foto nel modello Photo(ggogle drive)
                    photo_instance = Photo(
                        filename=generate_unique_filename(),
                        filetype=photo.content_type.split('/')[-1],
                        filesize=photo.size,
                        filedata=photo
                    )
                    photo_instance.save()
                   
                    user.photo = photo_instance
                    user.save()
                if serializer.is_valid():
                    

                    updated_user = serializer.save()
                    json_mapper = {
                        'id': str(updated_user.id),
                        'email': str(updated_user.email),
                        'first_name': str(updated_user.first_name),
                        'last_name': str(updated_user.last_name),
                        'data_iscrizione': str(updated_user.data_iscrizione),
                        'photo': str(get_direct_url(Photo.objects.filter(filename=updated_user.photo).first())),
                        'group': [group.name for group in user.groups.all()]
                    }
                
                return JsonResponse(json_mapper)
            except Exception as e: 
                print("Exception:", e)
                return JsonResponse({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)  
        else:
            return JsonResponse({"Error": "Impossible show the data of the user"}, status=response.status_code)        
        
class ManagerViewRegistration(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        print("post: " + str(request.data))
        if request.data is not None and request.data.get('p_iva') is not None:
            p_iva = request.data.get('p_iva')
            if not validate_partita_iva(p_iva):
                return JsonResponse({"Error": "Impossible register the p_iva is not correct"},status=status.HTTP_400_BAD_REQUEST)
            res =registerUser(request.data.get('email'), request.data.get('first_name'), request.data.get('password'), request.data.get('re_password'))
            if res.status_code != 201:
                return JsonResponse(json.loads(res.content), status=res.status_code)
            user_data = res.json()
            user = get_object_or_404(UserAccount, pk=user_data['id'])

            user.p_iva = p_iva
            user.save()
            manager_group = Group.objects.get(name="Manager")
            user.groups.add(manager_group)
            return JsonResponse({"id":user.pk, "email": user.email, "first_name": user.first_name},status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({"Error": "Impossible register the p_iva is not present"},status=status.HTTP_400_BAD_REQUEST)
    
class InvitoView(APIView):
    def get_search(self, request):
        invitations = Invito.objects.all()
        query_params = request.GET
        order_by = query_params.get('orderBy', '-exec_time')
        if query_params.get('obj.uuid') is not None:
            invitations=invitations.filter(uuid=query_params.get('obj.uuid'))
        if query_params.get('obj.status') is not None:
            invitations=invitations.filter(status=query_params.get('obj.status'))
        if query_params.get('obj.email') is not None:
            invitations=invitations.filter(email=query_params.get('obj.email'))
        else:
            invitations=invitations.filter(email=get_principal(request))
        if query_params.get('obj.employee_uuid') is not None:
            invitations=invitations.filter(employee_uuid=query_params.get('obj.employee_uuid'))
        if query_params.get('obj.center_uuid') is not None:
            invitations=invitations.filter(center_uuid=query_params.get('obj.center_uuid'))
        if query_params.get('from.exec_time') is not None:
            invitations=invitations.filter(start_date__gte=DateUtils.parse_string_to_datetime(query_params.get('from.exec_time')))
        if query_params.get('to.exec_time') is not None:
            invitations=invitations.filter(start_date__lte=DateUtils.parse_string_to_datetime(query_params.get('to.exec_time')))
        if query_params.get('obj.exec_time') is not None:
            invitations=invitations.filter(start_date=DateUtils.parse_string_to_datetime(query_params.get('obj.exec_time')))

        invitations = invitations.all().order_by(order_by)

        return invitations 

    def get(self, request):
        try:

            invitations = self.get_search(request)
            list_size = invitations.count()
            start_row = int(request.GET.get('startRow', 0))
            page_size = int(request.GET.get('pageSize', 10))
            if(page_size < 0):
                raise ValueError("the pageSize cannot be negative.")
            if(start_row < 0):
                raise ValueError("the startRow cannot be negative.")
            if(start_row > list_size):          #non restituisco nulla ma informo con l'header dei risultati
                return JsonResponse({"reviews": None}, headers={"listSize": str(list_size)})

            
            paginated_invitations = invitations[start_row:start_row + page_size]

            # Serializza i dati
            invitations_list = InvitationSerializer(paginated_invitations, many=True).data
            
            return JsonResponse({"invitations": invitations_list}, headers={"listSize": str(list_size)})
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except FieldError:
            return JsonResponse({"error": "Invalid orderBy parameter"}, status=400)

    def put(self, request, uuid):
        try:
            invitation = get_object_or_404(Invito, uuid=uuid)
            email=get_principal(request)
            if invitation.email != email:          
                return JsonResponse({"error": "Forbidden: the user that modified the invitation is not the recipient"}, status=403)
            data = json.loads(request.body)
        except ValidationError:
                return JsonResponse({"error": "Invalid UUID format"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        if uuid == str(data.get('uuid')):
            serializer = InvitationSerializer(invitation, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=200)
            return JsonResponse(serializer.errors, status=400)
        else:
            return JsonResponse({"error": "uuid must be the same."}, status=400)