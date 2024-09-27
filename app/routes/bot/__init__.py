from app.models import BotsCrawJUD, LicensesUsers
from flask import (Blueprint, request, url_for, redirect, current_app,
                   session, jsonify, make_response)
import os
import json
import pathlib
import platform
import threading
import subprocess
from clear import clear

path_template = os.path.join(pathlib.Path(__file__).parent.resolve(), "templates")
bot = Blueprint("bot", __name__, template_folder=path_template)


@bot.route("/bot/<id>/<system>/<type>", methods = ["POST"])
def botlaunch(id: int, system: str, type: str):

    pid = request.form.get("pid")
    path_pid = os.path.join(current_app.config["TEMP_PATH"], pid)
    os.makedirs(path_pid, exist_ok=True)
    
    for f, value in request.files.items():
        filesav = os.path.join(path_pid, f)
        value.save(filesav)
    
    data = {} 
    path_args = os.path.join(path_pid, f"{pid}.json")
    for key, value in request.form.items():
        data.update({key: value})
    
    data.update({
        "id": id,
        "system": system,
        "type": type
    })
    
    with open(path_args, "w") as f:
        f.write(json.dumps(data))       
        
    resp = make_response(jsonify({"ok": "ok"}), 200)
    inicia = threading.Thread(target=start_, args=(pid,))
    inicia.start()
    
    return resp

def start_(pid: str):
    
    clear()
    argumentos = [f"{pid}"]
    sistema = platform.system()
    
    if sistema == "Windows":
        path_python = ".venv/Scripts/python" 
        
    else:
        path_python = ".venv/bin/python"
        
    subprocess.run([path_python, "initbot.py"] + argumentos)

