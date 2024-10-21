from flask import Blueprint, request, jsonify, make_response

import os
import pytz
import json
import pathlib
from datetime import datetime

from app import db
from app import app
from app.models import ThreadBots
from app.models import Users, Executions
from app.misc.get_outputfile import get_file

from initbot import WorkerThread

path_template = os.path.join(pathlib.Path(__file__).parent.resolve(), "templates")
bot = Blueprint("bot", __name__, template_folder=path_template)

@bot.route("/bot/<id>/<system>/<typebot>", methods = ["POST"])
def botlaunch(id: int, system: str, typebot: str):
    
    from bot.head.Tools.StartStop_Notify import SetStatus
    with app.app_context():
        try:
            
            if request.data:
                data_bot = json.loads(request.data)
                
            elif request.form:
                data_bot = request.form
                
            if isinstance(data_bot, str):
                data_bot = json.loads(data_bot)
            
            start_rb = SetStatus(data_bot, request.files, id, system, typebot)
            path_args, display_name = start_rb.start_bot()
            worker_thread = WorkerThread()
            is_started = worker_thread.start(path_args, display_name)
            
        except Exception as e:
            is_started = 500    
        
    resp = make_response(jsonify({"ok": "ok"}), is_started)
    return resp

@bot.route('/stop/<user>/<pid>', methods=["POST"])
def stop_bot(user: str, pid: str):
    
    
    with app.app_context():
        set_stop = stop_execution(user, pid)
        
        if set_stop == 200:
        
            return jsonify({'Encerrado!': 'Sucesso'}), set_stop
        
        elif set_stop != 200:
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
                typebot = get_info.bot[0].type
                SetStatus(usr=user, pid=pid, system=system, typebot=typebot).botstop()
                return 200
            
            return 200
    except Exception as e:
        print(e)
        return 500

