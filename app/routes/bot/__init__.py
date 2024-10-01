from app.models import BotsCrawJUD, LicensesUsers, Users, Executions
from flask import (Blueprint, request, url_for, redirect,
                   session, jsonify, make_response)
import os
import json
import pathlib
import platform
import openpyxl
import threading
import subprocess
from clear import clear
from openpyxl.worksheet.worksheet import Worksheet

from app import app
from app import db


path_template = os.path.join(pathlib.Path(__file__).parent.resolve(), "templates")
bot = Blueprint("bot", __name__, template_folder=path_template)

@bot.route("/bot/<id>/<system>/<type>", methods = ["POST"])
def botlaunch(id: int, system: str, type: str):


    user = request.form.get("user")
    license_token = request.form.get("license_token")
    pid = request.form.get("pid")
    path_pid = os.path.join(app.config["TEMP_PATH"], pid)
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
    
    input_file = os.path.join(pathlib.Path(path_args).parent.resolve(), data['xlsx'])
    wb = openpyxl.load_workbook(filename=input_file)
    ws: Worksheet = wb.active
    rows = ws.max_row
    
    data.update({"total_rows": rows})
    
    with open(path_args, "w") as f:
        f.write(json.dumps(data))   
    
    resp = make_response(jsonify({"ok": "ok"}), 200)
    inicia = threading.Thread(target=start_, args=(path_args,))
    inicia.start()
    
    execut = Executions(
        pid = pid,
        status = "Em Execução",
        file_output = data.get("xlsx"),
        url_socket = data.get("url_socket"),
        total_rows = rows
    )
    
    usr = Users.query.filter(Users.login == user).first()
    bt = BotsCrawJUD.query.filter(BotsCrawJUD.id == id).first()
    
    execut.user.append(usr)
    execut.bot.append(bt)
    
    db.session.add(execut)
    db.session.commit()
    
    return resp

def start_(path_args: str):
    
    clear()
    with app.app_context():
        argumentos = [f"{path_args}"]
        sistema = platform.system()
        
        if sistema == "Windows":
            path_python = ".venv/Scripts/python" 
            
        else:
            path_python = ".venv/bin/python"
            
        subprocess.run([path_python, "initbot.py"] + argumentos)

