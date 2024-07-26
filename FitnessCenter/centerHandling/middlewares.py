import jwt
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from os import getenv
import requests

class UpdateAuthTokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        header_token = request.headers.get('Authorization')
        cookie_token = request.COOKIES.get('access')
        token = None
        if header_token:
            token = header_token.replace('Bearer', '').strip()
        elif cookie_token:
            token = cookie_token

        if token:
            response = requests.post(f"{getenv('SSO_URL', 'http://localhost:8000/')}api/jwt/verify", json={"token": token}, headers={"Content-Type": "application/json"})
            if response.status_code != 200:
                refresh_token = request.COOKIES.get('refresh')
                if refresh_token:
                    refresh_response = requests.post(f"{getenv('SSO_URL', 'http://localhost:8000/')}api/jwt/refresh", json={"refresh": refresh_token}, headers={"Content-Type": "application/json"})
                
                    token = refresh_response.json().get('access')
        
        request.META['Authorization'] = token
        request.COOKIES['access'] = token
        request.access_token = token
