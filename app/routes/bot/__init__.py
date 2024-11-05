from flask import Blueprint, request, jsonify, make_response

import os
import pytz
import json
import pathlib
import platform
from datetime import datetime

from app import db
from app import app
from app.models import ThreadBots
from app.models import Users, Executions
from app.misc.get_outputfile import get_file

from app.misc.get_location import GeoLoc
from bot import WorkerThread

path_template = os.path.join(pathlib.Path(__file__).parent.resolve(), "templates")
bot = Blueprint("bot", __name__, template_folder=path_template)


@bot.route("/bot/<id>/<system>/<typebot>", methods=["POST"])
def botlaunch(id: int, system: str, typebot: str):

    message = {"success": "success"}
    from status import SetStatus

    with app.app_context():
        try:

            loc = GeoLoc().region_name
            if request.data:
                data_bot = json.loads(request.data)

            elif request.form:
                data_bot = request.form

            if isinstance(data_bot, str):
                data_bot = json.loads(data_bot)

            if system == "esaj" and platform.system() != "Windows":
                raise Exception("Este servidor não pode executar este robô!")

            elif system == "caixa" and loc != "Amazonas":
                raise Exception("Este servidor não pode executar este robô!")

            start_rb = SetStatus(data_bot, request.files, id, system, typebot)
            path_args, display_name = start_rb.start_bot()
            worker_thread = WorkerThread(
                path_args=path_args,
                display_name=display_name,
                system=system,
                typebot=typebot,
            )
            is_started = worker_thread.start()

        except Exception as e:
            message = {"error": str(e)}
            is_started = 500

    resp = make_response(jsonify(message), is_started)
    return resp


@bot.route("/stop/<user>/<pid>", methods=["POST"])
def stop_bot(user: str, pid: str):

    with app.app_context():
        set_stop = stop_execution(user, pid)

        if set_stop == 200:

            return jsonify({"Encerrado!": "Sucesso"}), set_stop

        elif set_stop != 200:
            return jsonify({"mensagem": "erro"}), set_stop


def stop_execution(user: str, pid: str) -> int:

    try:

        processID = ThreadBots.query.filter(ThreadBots.pid == pid).first()

        if processID:
            processID = int(processID.processID)
            worker_thread = WorkerThread().stop(processID, pid)
            app.logger.info(worker_thread)
            from status import SetStatus

            user_id = Users.query.filter(Users.login == user).first().id
            get_info = (
                db.session.query(Executions)
                .join(Users, Users.id == user_id)
                .filter(Executions.pid == pid)
                .first()
            )

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
                SetStatus(usr=user, pid=pid, system=system, typebot=typebot).botstop()
                return 200

            return 200
    except Exception as e:
        app.logger.error(str(e))
        return 500
