from datetime import datetime, date
from dateutil import parser
import re

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