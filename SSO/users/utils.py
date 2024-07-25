import uuid
import requests
from os import getenv
import json
from datetime import datetime, date
from dateutil import parser
import re
import jwt 
from django.conf import settings
def generate_unique_filename():
    # Genera un UUID4 (Universally Unique Identifier version 4)

    # Formatta l'UUID come stringa e ritorna il nome del file
    filename = uuid.uuid4() 
    return filename

def get_principal(request):
    token=None
    if request.headers and request.headers.get('Authorization'):
        token = request.headers.get('Authorization').split()[1]
    if not token:
        return None
    payload = jwt.decode(token.encode('UTF-8'), settings.SECRET_KEY, algorithms=['HS256'])
    if not payload: 
        return None
    email = payload.get('email')
    return email

def validate_partita_iva(p_iva):
    
    if not p_iva.isdigit() or len(p_iva) != 11:
        return False
    
    digits = [int(char) for char in p_iva]

    odd_sum = sum(digits[i] for i in range(0, 10, 2))

    even_sum = 0

    for i in range(1, 10, 2):
        even_digit = digits[i] * 2
        if even_digit > 9:
            even_digit = even_digit - 9
        even_sum += even_digit

    total_sum = odd_sum + even_sum

    check_digit = (10 - (total_sum % 10)) % 10

    return check_digit == digits[10]


def registerUser(email, first_name, password, re_password):
    url = f"{getenv('DJANGO_SERVER_HOST')}/api/users/"
    headers = {
        'Content-Type': 'application/json',
    }
    payload = {
        'email': email,
        'first_name': first_name,
        'password': password,
        're_password': re_password
    }
    return requests.post(url=url, headers=headers,data=(json.dumps(payload)))

class DateUtils():
    
    date_patterns = [
            re.compile(r'^\d{4}-\d{2}-\d{2}$'),  # yyyy-MM-dd
            re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'),  # yyyy-MM-dd'T'HH:mm:ss
            re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$')  # yyyy-MM-dd'T'HH:mm:ss.SSSZ
        ]

    @classmethod
    def parse_string_to_date(cls, s):
        if any(pattern.match(s) for pattern in cls.date_patterns):
            # Usa dateutil per parsare la stringa in un oggetto datetime
            dt = parser.parse(s)
            # Ritorna solo la parte di data (yyyy-MM-dd)
            return dt.date()
        else:
            raise ValueError("Date format is not supported")
        

    @classmethod
    def parse_string_to_datetime(cls, s):
        if any(pattern.match(s) for pattern in cls.date_patterns):
            
            dt = parser.parse(s)

            return dt
        else:
            raise ValueError("Date format is not supported")