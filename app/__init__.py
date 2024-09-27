from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from flask_socketio import SocketIO
from app import default_config
from configs import csp

import os
import pathlib
from datetime import timedelta

src_path = os.path.join(os.getcwd(), "static")
app = Flask(__name__, static_folder=src_path)

app.config.from_object(default_config)
db = SQLAlchemy()
tlsm = Talisman()
mail = Mail()
io = SocketIO()

def init_app() -> None:
    
    from app.models import init_database
    age = timedelta(days=31).max.seconds
    db.init_app(app)
    mail.init_app(app)
    io.init_app(app)
    
    tlsm.init_app(app, content_security_policy=csp(),
                session_cookie_http_only=True,
                session_cookie_samesite='Lax',
                strict_transport_security=True,
                strict_transport_security_max_age=age,
                x_content_type_options= True,
                x_xss_protection=True)
    init_database()
    
init_app()

from app import routes
