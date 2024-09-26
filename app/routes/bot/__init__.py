from app.models import BotsCrawJUD, LicensesUsers
from flask import (Blueprint, request, url_for, redirect, 
                   session, jsonify, make_response)
import os
import pathlib


path_template = os.path.join(pathlib.Path(__file__).parent.resolve(), "templates")
bot = Blueprint("bot", __name__, template_folder=path_template)


@bot.route("/bot/<id>/<system>/<type>")
def botlaunch(id: int, system: str, type: str):

    resp = make_response(jsonify({"ok": "ok"}), 200)
    return resp
