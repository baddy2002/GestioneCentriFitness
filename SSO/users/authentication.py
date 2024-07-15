from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(cls, user):
        token = super().get_token(user)
        # Aggiungi gruppi al token
        token['groups'] =  [group.name for group in user.groups.all()] 
        token['full_name'] = user.first_name + user.last_name
        token['email'] = user.email
        
        return token


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            header = self.get_header(request)
            if header is None:
                raw_token = request.COOKIES.get('access')
            else:
                raw_token = self.get_raw_token(header)
            
            if raw_token is None:
                return None

            validated_token = self.get_validated_token(raw_token)

            return self.get_user(validated_token), validated_token
        except:
            return None
