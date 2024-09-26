from app import db
from app import app

from app.models.users import Users, LicensesUsers
from app.models.bots import BotsCrawJUD, Credentials
from app.models.srv import Servers

import pandas as pd
from uuid import uuid4

def init_database():
    
    with app.app_context():
        db.create_all()
        
        