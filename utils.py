import secrets
import string

def generate_secret_key(lenght=24):
    alphabet = string.ascii_letters +  string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(lenght))