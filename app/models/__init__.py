from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app import app, db
from app.models.users import Users, LicensesUsers
from app.models.bots import BotsCrawJUD, Credentials, Executions, CacheLogs, ThreadBots
from app.models.srv import Servers

import platform
import pandas as pd
from uuid import uuid4
from dotenv import dotenv_values
def init_database():
    
    values = dotenv_values()
    with app.app_context():
        
        db.create_all()
        
        NAMESERVER = values.get("NAMESERVER")
        HOST = values.get("HOST")
        
        if not Servers.query.filter(Servers.name == NAMESERVER).first():
        
            server = Servers(
                name = NAMESERVER,
                address = HOST,
                system = platform.system()
            )
            db.session.add(server)
            db.session.commit()
            
        
        
        