from datetime import datetime, date, timedelta
from dateutil import parser
import re

class DateUtils():
    
    date_patterns = [
            re.compile(r'^\d{4}-\d{2}-\d{2}$'),  # yyyy-MM-dd
            re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'),  # yyyy-MM-dd'T'HH:mm:ss
            re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$'),  # yyyy-MM-dd'T'HH:mm:ss.SSSZ
            re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.+\d{2}:\d{2}$')  # yyyy-MM-dd'T'HH:mm:ss.SSSZ
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
        
    @classmethod
    def generate_slots(cls, start_time, end_time, date=None):
        # Converti start_time e end_time in datetime.datetime per la manipolazione
        if date == None:
            date = datetime.now().date()
        start_datetime = datetime.combine(date, start_time)
        end_datetime = datetime.combine(date, end_time)
        
        # Validazione degli orari
        if start_datetime >= end_datetime:
            raise ValueError("L'orario di inizio deve essere precedente all'orario di fine.")
        
        # Crea una lista per gli intervalli di mezz'ora
        slots = []
        
        current_time = start_datetime
        while current_time < end_datetime:
            next_time = current_time + timedelta(minutes=30)
            slots.append((current_time.time(), next_time.time()))
            current_time = next_time
        
        return slots


