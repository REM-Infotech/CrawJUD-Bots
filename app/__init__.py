## Flask imports
from flask import Flask
from flask_mail import Mail
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman

## Python Imports
import os
import re
from dotenv import dotenv_values
from datetime import timedelta


## APP Imports
from configs import csp
from app import default_config

src_path = os.path.join(os.getcwd(), "static")

db = SQLAlchemy()
tlsm = Talisman()
mail = Mail()
io = SocketIO()
app = Flask(__name__, static_folder=src_path)
app.config.from_object(default_config)

allowed_origins = [
    r"https:\/\/.*\.nicholas\.dev\.br",
    r"https:\/\/.*\.robotz\.dev",
    r"https:\/\/.*\.rhsolutions\.info",
    r"https:\/\/.*\.rhsolut\.com\.br"
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

def init_app():
    
    age = timedelta(days=31).max.seconds
    db.init_app(app)
    mail.init_app(app)
    io.init_app(app, cors_allowed_origins=check_allowed_origin)
    tlsm.init_app(app, content_security_policy=csp(),
                session_cookie_http_only=True,
                session_cookie_samesite='Lax',
                strict_transport_security=True,
                strict_transport_security_max_age=age,
                x_content_type_options= True,
                x_xss_protection=True)
    
    with app.app_context():
        from app.models import init_database
        init_database()
        
from app import routes
init_app()
