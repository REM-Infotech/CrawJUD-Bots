from google.cloud import storage
from google.oauth2 import service_account

from dotenv import dotenv_values
import json

def enviar_arquivo_para_gcs(arquivo_local, objeto_destino) -> bool:
        
    try:
        bucket_name = "outputexec-bots"
        project_id = "modular-hulling-404421"
        # Inicializa o cliente GCS
        
        credentials_dict = json.loads(dotenv_values().get("credentials_dict"))
        
        credentials = service_account.Credentials.from_service_account_info(
            credentials_dict)
        scoped_credentials = credentials.with_scopes(
            ['https://www.googleapis.com/auth/cloud-platform'])
        
        
        
        storage_client = storage.Client(
            credentials=scoped_credentials, project=project_id)

        # Obtém o bucket
        bucket = storage_client.bucket(bucket_name)

        # Cria um objeto Blob no bucket
        blob = bucket.blob(objeto_destino)

        # Faz o upload do arquivo local para o objeto Blob
        blob.upload_from_filename(arquivo_local)
        
        return True
        
    except Exception as e:
        
        return False