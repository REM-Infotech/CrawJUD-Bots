from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.models.users import Users, LicensesUsers
from app.models.bots import BotsCrawJUD, Credentials
from app.models.srv import Servers

import pandas as pd
from uuid import uuid4

def init_database(app: Flask, db: SQLAlchemy):
    
    with app.app_context():
        db.create_all()
        
        