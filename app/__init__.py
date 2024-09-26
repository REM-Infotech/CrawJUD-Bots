from flask import Flask
from flask_mail import Mail
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from app import default_config
from configs import csp

import os
import pathlib
from datetime import timedelta

src_path = os.path.join(os.getcwd(), "static")
app = Flask(__name__, static_folder=src_path)

os.makedirs("logs", exist_ok=True)
os.makedirs("Archives", exist_ok=True)

app.config.from_object(default_config)

mail = Mail()
db = SQLAlchemy()
socketio = SocketIO()

def init_app() -> None:
    
    from app.models import init_database
    db.init_app(app)
    mail.init_app(app)
    socketio.init_app(app)
    init_database()
    
init_app()

from app import routes
