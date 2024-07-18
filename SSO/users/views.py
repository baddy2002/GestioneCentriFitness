from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from djoser.social.views import ProviderAuthView
import jwt
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from django.shortcuts import get_object_or_404
from os import getenv
from .models import UserAccount, Photo
from .authentication import CustomTokenObtainPairSerializer
import requests
import json
from django.http import JsonResponse
from .serializers import UserAccountSerializer
from .utils import generate_unique_filename
import base64

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
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
            response.set_cookie(
                'refresh',
                refresh_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
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
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
            response.set_cookie(
                'refresh',
                refresh_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
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
        url = 'http://127.0.0.1:8000/api/users/me/' 
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
                'photo': direct_url if direct_url is not None else None
            }
            return JsonResponse(json_mapper)
        else:
            return JsonResponse({"Error": "Impossible show the data of the user"})
        
    def put(self, request, *args, **kwargs):
        print(request.FILES)
        url = 'http://127.0.0.1:8000/api/users/me/' 
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
                        'photo': str(get_direct_url(Photo.objects.filter(filename=updated_user.photo).first()))
                    }
                
                return JsonResponse(json_mapper)
            except Exception as e: 
                print("Exception:", e)
                return JsonResponse({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)  
        else:
            return JsonResponse({"Error": "Impossible show the data of the user"}, status=response.status_code)        
        

    