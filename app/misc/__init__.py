import json
import random
import string
from dotenv import dotenv_values
from google.oauth2.service_account import Credentials
from google.cloud.storage import Client, Bucket

signed_url_lifetime = 300

import pytz
from app import db, app
from datetime import datetime
from app.models import ThreadBots
from app.models import Users, Executions
from app.misc.get_outputfile import get_file
from bot import WorkerThread
from .get_location import GeoLoc

__all__ = [GeoLoc]


def generate_pid() -> str:

    while True:
        # Gerar 4 letras maiúsculas e 4 dígitos
        letters = random.sample(string.ascii_uppercase, 6)
        digits = random.sample(string.digits, 6)

        # Intercalar letras e dígitos
        pid = "".join(
            [letters[i // 2] if i % 2 == 0 else digits[i // 2] for i in range(6)]
        )

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
    return Credentials.from_service_account_info(credentials_dict).with_scopes(
        ["https://www.googleapis.com/auth/cloud-platform"]
    )

    # Configure a autenticação para a conta de serviço do GCS


def bucketGcs(storageClient: Client, bucket_name: str = None) -> Bucket:

    if not bucket_name:
        bucket_name = dotenv_values().get("bucket_name")

    bucket_obj = storageClient.bucket(bucket_name)
    return bucket_obj


def stop_execution(pid: str) -> int:

    from status import SetStatus

    try:

        processID = ThreadBots.query.filter(ThreadBots.pid == pid).first()

        if processID:
            processID = int(processID.processID)
            worker_thread = WorkerThread().stop(processID, pid)
            app.logger.info(worker_thread)

            get_info = (
                db.session.query(Executions).filter(Executions.pid == pid).first()
            )
            user = get_info.user.login

            filename = get_file(pid)
            if filename != "":
                get_info.status = "Finalizado"
                get_info.file_output = filename
                get_info.data_finalizacao = datetime.now(
                    pytz.timezone("America/Manaus")
                )
                db.session.commit()
                db.session.close()
                return 200

            elif filename == "":
                system = get_info.bot.system
                typebot = get_info.bot.type
                get_info.file_output = SetStatus(
                    usr=user, pid=pid, system=system, typebot=typebot
                ).botstop()
                db.session.commit()
                db.session.close()
                return 200

            return 200

    except Exception as e:
        app.logger.error(str(e))
        return 500
