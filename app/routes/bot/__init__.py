import multiprocessing.process
from app.models import BotsCrawJUD, LicensesUsers, Users, Executions
from flask import (Blueprint, request, url_for, redirect,
                   session, jsonify, make_response)
import os
import pytz
import json
import psutil
import pathlib
import platform
from datetime import datetime

import subprocess
from clear import clear
from initbot import WorkerThread

from app import db
from app import app
from app.models import ThreadBots
from app.misc.get_outputfile import get_file


path_template = os.path.join(pathlib.Path(__file__).parent.resolve(), "templates")
bot = Blueprint("bot", __name__, template_folder=path_template)

@bot.route("/bot/<id>/<system>/<type>", methods = ["POST"])
def botlaunch(id: int, system: str, type: str):
    
    from bot.head.Tools.StartStop_Notify import SetStatus
    with app.app_context():
        start_rb = SetStatus(request.form, request.files, id, system, type)
        path_args, display_name = start_rb.start_bot()
        worker_thread = WorkerThread()
        is_started = worker_thread.start(path_args, display_name)
    resp = make_response(jsonify({"ok": "ok"}), is_started)
    return resp

@bot.route('/stop/<user>/<pid>', methods=["POST"])
def stop_bot(user: str, pid: str):
    
    
    with app.app_context():
        set_stop = stop_execution(user, pid)
        
        if set_stop == 200:
        
            return jsonify({'Encerrado!': 'Sucesso'}), set_stop
        
        else:
            return jsonify({'mensagem': 'erro'}), set_stop

def stop_execution(user: str, pid: str) -> int:

    try:
        
        thread_id = ThreadBots.query.filter(
            ThreadBots.pid == pid).first()
        
        if thread_id:
            thread_id = int(thread_id.thread_id)
            worker_thread = WorkerThread()
            worker_thread.thread_id = thread_id
            worker_thread.stop()
        
        
            from bot.head.Tools.StartStop_Notify import SetStatus
            user_id = Users.query.filter(Users.login == user).first().id
            get_info = db.session.query(Executions).join(Executions.user).filter(
                    Users.id == user_id,  # Supondo que você também queira filtrar por um user_id específico
                    Executions.pid == pid
            ).first()
            
            filename = get_file(pid)
            if filename != "":
                get_info.status = 'Finalizado'
                get_info.file_output = filename
                get_info.data_finalizacao = datetime.now(pytz.timezone('Etc/GMT+4'))
                db.session.commit()
                db.session.close()
                return 200
            
            elif filename == "":
                system = get_info.bot[0].system
                type = get_info.bot[0].type
                SetStatus(usr=user, pid=pid, system=system, type=type).botstop()
                return 200
            
            return 200
    except Exception as e:
        print(e)
        return 500

