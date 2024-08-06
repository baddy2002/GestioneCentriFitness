# Usa un'immagine base di Python
FROM python:3.11

# Imposta la directory di lavoro
WORKDIR /app

# Copia il file delle dipendenze e installale
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia tutto il codice dell'applicazione
COPY . .

# Espone la porta 8000 per il server Django
EXPOSE 8000

# Comando di default per eseguire l'applicazione
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
