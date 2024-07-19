import uuid
import requests
from os import getenv
import json

def generate_unique_filename():
    # Genera un UUID4 (Universally Unique Identifier version 4)

    # Formatta l'UUID come stringa e ritorna il nome del file
    filename = uuid.uuid4() 
    return filename


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

