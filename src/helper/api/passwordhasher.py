import hmac
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

def hash_password(plain_password):
    API_SECRET = os.getenv('MOPH_API_SECRET')
    enc_password = hmac.new(bytes(API_SECRET, 'utf-8'), bytes(plain_password, 'utf-8'), digestmod=hashlib.sha256).hexdigest().upper()
    return(enc_password)