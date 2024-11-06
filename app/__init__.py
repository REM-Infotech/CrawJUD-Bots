# Flask imports
from flask import Flask
from flask_mail import Mail
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman

# Python Imports
import os
import re
from clear import clear
from dotenv import dotenv_values
from datetime import timedelta


# APP Imports
from configs import csp
from app import default_config


src_path = os.path.join(os.getcwd(), "static")
app = Flask(__name__, static_folder=src_path)
app.config.from_object(default_config)

db = SQLAlchemy()
mail = Mail()
io = SocketIO()

mail.init_app(app)
db.init_app(app)

clean_prompt = False

allowed_origins = [
    r"https:\/\/.*\.nicholas\.dev\.br",
    r"https:\/\/.*\.robotz\.dev",
    r"https:\/\/.*\.rhsolutions\.info",
    r"https:\/\/.*\.rhsolut\.com\.br",
]


def check_allowed_origin(origin: str = "https://google.com"):

    if not origin:
        origin = f'https://{dotenv_values().get("HOST")}'

    for orig in allowed_origins:
        pattern = orig
        matchs = re.match(pattern, origin)
        if matchs:
            return True

    return False


class CustomTalisman(Talisman):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_headers(self, response):
        super().set_headers(response)


class init_app:

    def __call__(self):
        with app.app_context():

            global clean_prompt
            if clean_prompt is False:
                clear()
                clean_prompt = True

            age = timedelta(days=31).max.seconds

            from app.models import init_database

            init_database()()

            io.init_app(app, cors_allowed_origins=check_allowed_origin)
            CustomTalisman(
                app,
                content_security_policy=csp(),
                session_cookie_http_only=True,
                session_cookie_samesite="Lax",
                strict_transport_security=True,
                strict_transport_security_max_age=age,
                x_content_type_options=True,
                x_xss_protection=True,
            )

    from app import routes
    from app import handling


init_app()()
