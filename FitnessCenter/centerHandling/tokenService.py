from os import getenv
from django.http import JsonResponse
import requests
from functools import wraps
import jwt


def jwt_base_authetication(view):
    @wraps(view)
    def wrapper(self, request, *args, **kwargs):
        if not hasattr(request, 'headers') or not hasattr(request, 'COOKIES'):
            return JsonResponse({"error":"Unauthorized, authentication data not provided"}, status=401)
        header_token=request.headers.get('Authorization')
        cookie_token=request.COOKIES.get('access')
        if header_token is not None:
            token = str(header_token).replace('Bearer', '').strip()
        elif cookie_token is not None:
            token=cookie_token
        else:
            return JsonResponse({"error":"Unauthorized, authentication data not provided"}, status=401)
        response = requests.post(f"{getenv('SSO_URL', 'http://localhost:8000/')}api/jwt/verify", json={"token":token}, headers={"Content-Type":"application/json"})
        if response.status_code != 200:
            refresh = request.COOKIES.get('refresh')
            
            if refresh is None:
                return JsonResponse({"error":"Unauthorized, authentication data not correct"}, status=401)
            response = requests.post(f"{getenv('SSO_URL', 'http://localhost:8000/')}api/jwt/refresh", json={"refresh":refresh}, headers={"Content-Type":"application/json"})
            if response.status_code != 200:
                return JsonResponse({"error":"Unauthorized, authentication data not correct"}, status=401)
            token=response.json().get('access')
        
        request.access = token

        return view(self, request, *args, **kwargs)
    return wrapper


def jwt_trainer_authetication(view):
    @wraps(view)
    def wrapper(self, request, *args, **kwargs):
        @jwt_base_authetication
        def wrapped_view(self, request, *args, **kwargs):
            access = getattr(request, 'access', None)
            try:
                payload = jwt.decode(access, getenv('DJANGO_SSO_SECRET_KEY'), algorithms=["HS256"])
                if 'groups' not in payload or all(group not in ['trainer', 'mixed', 'admin'] for group in payload['groups']):
                    return JsonResponse({"error": "Forbidden, insufficient permissions"}, status=403)
            except jwt.ExpiredSignatureError:
                return JsonResponse({"error": "Token has expired"}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({"error": "Invalid token"}, status=401)
            return view(self, request, *args, **kwargs)
        
        return wrapped_view(self, request, *args, **kwargs)
    return wrapper



def jwt_nutritionist_authetication(view):
    @wraps(view)
    def wrapper(self, request, *args, **kwargs):
        @jwt_base_authetication
        def wrapped_view(self, request, *args, **kwargs):
            access = getattr(request, 'access', None)
            try:
                payload = jwt.decode(access, getenv('DJANGO_SSO_SECRET_KEY'), algorithms=["HS256"])
                if 'groups' not in payload or all(group not in ['nutritionist', 'mixed', 'admin'] for group in payload['groups']): 
                    return JsonResponse({"error": "Forbidden, insufficient permissions"}, status=403)
            except jwt.ExpiredSignatureError:
                return JsonResponse({"error": "Token has expired"}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({"error": "Invalid token"}, status=401)
            return view(self, request, *args, **kwargs)
        
        return wrapped_view(self, request, *args, **kwargs)
    return wrapper

def jwt_manager_authetication(view):
    @wraps(view)
    def wrapper(self, request, *args, **kwargs):
        @jwt_base_authetication
        def wrapped_view(self, request, *args, **kwargs):
            access = getattr(request, 'access', None)
            try:
                payload = jwt.decode(access, getenv('DJANGO_SSO_SECRET_KEY'), algorithms=["HS256"])
                if 'groups' not in payload or all(group not in ['manager', 'admin'] for group in payload['groups']):
                    return JsonResponse({"error": "Forbidden, insufficient permissions"}, status=403)
            except jwt.ExpiredSignatureError:
                return JsonResponse({"error": "Token has expired"}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({"error": "Invalid token"}, status=401)
            return view(self, request, *args, **kwargs)
        
        return wrapped_view(self, request, *args, **kwargs)
    return wrapper