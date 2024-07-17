import uuid

def generate_unique_filename():
    # Genera un UUID4 (Universally Unique Identifier version 4)

    # Formatta l'UUID come stringa e ritorna il nome del file
    filename = uuid.uuid4() 
    return filename