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

import threading
import subprocess
from clear import clear


from app import app
from app import db
from app.misc.get_outputfile import get_file
from initbot import initBot

path_template = os.path.join(pathlib.Path(__file__).parent.resolve(), "templates")
bot = Blueprint("bot", __name__, template_folder=path_template)

@bot.route("/bot/<id>/<system>/<type>", methods = ["POST"])
def botlaunch(id: int, system: str, type: str):
    
    from bot.head.Tools.StartStop_Notify import SetStatus
    with app.app_context():
        start_rb = SetStatus(request.form, request.files, id, system, type)
        path_args = start_rb.start_bot()
        inicia = threading.Thread(target=start_, args=(path_args,))
        inicia.start()

    resp = make_response(jsonify({"ok": "ok"}), 200)
    return resp

@bot.route('/stop/<user>/<pid>', methods=["POST"])
def stop_bot(user: str, pid: str):
    
    
    with app.app_context():
        set_stop = stop_execution(user, pid)
        
        if set_stop == 200:
        
            return jsonify({'Encerrado!': 'Sucesso'}), set_stop
        
        else:
            return jsonify({'mensagem': 'erro'}), set_stop


def start_(path_args: str):
    
    clear()
    
    with app.app_context():
        initBot(path_args)

def stop_execution(user: str, pid: str) -> int:

    try:
        
        from bot.head.Tools.StartStop_Notify import SetStatus
        user_id = Users.query.filter(Users.login == user).first().id
        get_info = db.session.query(Executions).join(Executions.user).filter(
                Users.id == user_id,  # Supondo que você também queira filtrar por um user_id específico
                Executions.pid == pid
        ).first()
        
        filename = get_file(pid)
        if get_info.status == 'Finalizado':
            return 200
        
        elif get_info.status != 'Finalizado':
            
            if filename != "":
                
                get_info.status = 'Finalizado'
                get_info.file_output = filename
                get_info.data_finalizacao = datetime.now(pytz.timezone('Etc/GMT+4'))
                db.session.commit()
                db.session.close()
                return 200
            

            try:
                
                get_process = psutil.process_iter(['cmdline'])
                
                for process in get_process:
                    infoproc = process.info['cmdline']
                    
                    if infoproc is None:
                        continue
                    
                    for item_cmd in infoproc:
                    
                        if pid in item_cmd:
                            try:
                                process.kill()
                            except psutil.NoSuchProcess as e:
                                break
                            
                        
            except Exception as e:
                pass
            
            system = get_info.bot[0].system
            type = get_info.bot[0].type
            SetStatus(usr=user, pid=pid, system=system, type=type).botstop()
            return 200
        
    except Exception as e:
        print(e)
        return 500

