import code
import jwt
import os
import urllib.request 
import urllib.parse
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class AuthenticateTokenManager:
    def __init__(self):
        self.__token = None
        self.__fetch_time = None

    @property
    def token(self):
        return self.__token

    @staticmethod
    def GetJWTFromMOPH(user, hash_password, hospital_code):
        url = os.getenv('MOPH_API_BASE_URL') + os.getenv('MOPH_TOKEN_ENDPOINT')
        payload = {'Action': os.getenv('MOPH_TOKEN_ENDPOINT_ACTION'), 'user': user, 'password_hash': hash_password, 'hospital_code': hospital_code}
        qs = urllib.parse.urlencode(payload)
        url = url + '?' + qs
        try:
            with urllib.request.urlopen(url) as response:
                return response.read().decode('utf-8')
        except urllib.error.HTTPError as e:
            message = 'Unable to Authenticate: {}'.format(e.code)
            raise Exception(message)

    def generate_bearer_auth_header(self):
        headers = []
        headers["Accept"] = "application/json"
        headers["Authorization"] = "Bearer {}".format(self.__token)
        return headers
    
    def get_token_from_moph(self, user, hash_password, hospital_code):
        token = AuthenticateTokenManager.GetJWTFromMOPH(user, hash_password, hospital_code)
        print(token)
        if token:
            self.__token = token
            self.__fetch_time = datetime.now()
            return 1
        else:
            return 0

    def refresh_token(self, user, hash_password, hospital_code):
        if self.__token:
            duration_in_secs = datetime.now() - self.__fetch_time
            if divmod(duration_in_secs, 3600)[0] > 6:
                self.get_token_from_moph(user, hash_password, hospital_code)


class JWTVerifier:
    @staticmethod
    def decoded_jwt(jwt_response, pub_key):
        try:
            decoded_data = jwt.decode(jwt_response, key = pub_key, audience="MOPH API", algorithms="RS512", options = {"verify_signature": True})
            #Extract ['client']['name'] and back to verify login // don't need since jwt already verified it self.
            return decoded_data
        except:
            raise


class PublicKeyManager:
    @staticmethod
    def try_read_key_from_file(filepath = os.path.abspath(os.curdir) + '/key/pubkey.pub'):
        try:
            with open(filepath) as key:
                return key.read()
        except:
            PublicKeyManager.get_pubkey_from_api()

    @staticmethod
    def get_pubkey_from_api():
        url = "https://cvp1.moph.go.th/token?Action=get_public_key"
        try:
            response = urllib.request.urlopen(url)
            filepath = '{curpath}/key/pubkey.pub'.format('curpath', os.path.abspath(os.curdir))
            key_content = response.read()
            if key_content is not None:
                PublicKeyManager.save_as_file(filepath, key_content)
                return key_content
            else:
                raise Exception("Public Key is invalid. It's empty")                
        except:
            raise
        
    @staticmethod
    def save_as_file(filepath, content):
        try:
            with open(filepath, "wb") as file:
                file.write(content)
        except FileNotFoundError:
           os.makedirs(os.path.dirname(filepath))
           PublicKeyManager.save_as_file(filepath, content)
