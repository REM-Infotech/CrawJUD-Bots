import json
import random
import string
from dotenv import dotenv_values
from google.oauth2.service_account import Credentials
from google.cloud.storage import Client, Bucket

signed_url_lifetime = 300
def generate_pid() -> str:
    
    while True:
        # Gerar 4 letras maiúsculas e 4 dígitos
        letters = random.sample(string.ascii_uppercase, 6)
        digits = random.sample(string.digits, 6)

        # Intercalar letras e dígitos
        pid = ''.join([letters[i//2] if i % 2 == 0 else digits[i//2] for i in range(6)])

        # Verificar se a string gerada não contém sequências do tipo "AABB"
        if not any(pid[i] == pid[i + 1] for i in range(len(pid) - 1)):
            return pid
        
def storageClient() -> Client:
    
    project_id = dotenv_values().get("project_id")
    # Configure a autenticação para a conta de serviço do GCS
    credentials = CredentialsGCS()

    return Client(credentials=credentials, project=project_id)

def CredentialsGCS() -> Credentials:
    
    credentials_dict = json.loads(dotenv_values().get("credentials_dict"))
    return Credentials.from_service_account_info(
        credentials_dict).with_scopes(['https://www.googleapis.com/auth/cloud-platform'])
    
    # Configure a autenticação para a conta de serviço do GCS

def bucketGcs(storageClient: Client, bucket_name: str = None) -> Bucket:
    
    if not bucket_name:
        bucket_name = dotenv_values().get("bucket_name")
        
    bucket_obj = storageClient.bucket(bucket_name)  
    return bucket_obj