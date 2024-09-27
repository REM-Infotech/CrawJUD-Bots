## Flask imports
from flask import Flask
from flask_mail import Mail
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman

## Python Imports
import os
from dotenv import dotenv_values
from datetime import timedelta


## APP Imports
from configs import csp
from app import default_config


db = SQLAlchemy()
tlsm = Talisman()
mail = Mail()
io = SocketIO()

def create_app() -> tuple[Flask, int, bool]:

    src_path = os.path.join(os.getcwd(), "static")
    app = Flask(__name__, static_folder=src_path)

    app.config.from_object(default_config)
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
    
    from app.models import init_database
    from app.routes import  blueprint_reg
    
    init_database(app, db)
    blueprint_reg(app, io)
    values = dotenv_values()
    
    ## Cloudflare Tunnel Configs
    hostname = values.get("HOSTNAME")
    port = int(values.get("PORT", 5000))
    debug = values.get('DEBUG', 'False').lower() in (
        'true', '1', 't', 'y', 'yes')
    
    
    return (app, port, debug, io)


