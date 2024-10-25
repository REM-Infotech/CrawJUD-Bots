from app import app
from flask import redirect
from werkzeug.exceptions import HTTPException
from dotenv import dotenv_values


@app.errorhandler(HTTPException)
def handle_http_exception(error):

    url = dotenv_values().get("url_web")
    return redirect(url)
