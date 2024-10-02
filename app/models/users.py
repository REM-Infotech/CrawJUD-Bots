from flask import request
from uuid import uuid4
from datetime import datetime
import bcrypt
from app import db
import pytz
salt = bcrypt.gensalt()

admins = db.Table(
    'admins', 
    db.Column('license_user_id', db.Integer, db.ForeignKey('licenses_users.id'), primary_key=True),
    db.Column('users_id', db.Integer, db.ForeignKey('users.id'), primary_key=True))

licenseusr = db.Table(
    'licenseusr', 
    db.Column('license_user_id', db.Integer, db.ForeignKey('licenses_users.id'), primary_key=True),
    db.Column('users_id', db.Integer, db.ForeignKey('users.id'), primary_key=True))

licenses_users_bots = db.Table(
    'licenses_users_bots',
    db.Column('licenses_user_id', db.Integer, db.ForeignKey('licenses_users.id'), primary_key=True),
    db.Column('bot_id', db.Integer, db.ForeignKey('bots.id'), primary_key=True)
)

# Tabela de associação para LicensesUsers e Credentials
licenses_users_credentials = db.Table(
    'licenses_users_credentials',
    db.Column('license_user_id', db.Integer, db.ForeignKey('licenses_users.id'), primary_key=True),
    db.Column('credential_id', db.Integer, db.ForeignKey('credentials.id'), primary_key=True)
)

class Users(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(length=30), nullable=False, unique=True)
    nome_usuario = db.Column(db.String(length=64), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    password = db.Column(db.String(length=60), nullable=False)
    login_time = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Etc/GMT+4')))
    verification_code = db.Column(db.String(length=45), unique=True)
    login_id = db.Column(db.String(length=64), nullable=False, default=str(uuid4()))
    filename = db.Column(db.String(length=128))
    blob_doc = db.Column(db.LargeBinary(length=(2**32)-1))

    def __init__(self, login: str = None, nome_usuario: str = None,
                 email: str = None, license_key: str = None) -> None:

        self.login = login
        self.nome_usuario = nome_usuario
        self.email = email

    @property
    def senhacrip(self):
        return self.senhacrip

    @senhacrip.setter
    def senhacrip(self, senha_texto: str):
        self.password = bcrypt.hashpw(
            senha_texto.encode(), salt).decode("utf-8")

    def check_password(self, senha_texto_claro: str) -> bool:
        return bcrypt.checkpw(senha_texto_claro.encode("utf-8"), self.password.encode("utf-8"))

class LicensesUsers(db.Model):
    
    __tablename__ = 'licenses_users'
    id = db.Column(db.Integer, primary_key=True)
    name_client = db.Column(db.String(length=60), nullable=False, unique=True)
    cpf_cnpj = db.Column(db.String(length=30), nullable=False, unique=True)
    license_token = db.Column(db.String(length=512), nullable=False, unique=True)
    
    # Relacionamento de muitos para muitos com users
    users = db.relationship('Users', secondary=licenseusr, backref='licenses')
    admins = db.relationship('Users', secondary=admins, backref='admin')
    
    # Relacionamento de muitos para muitos com Credentials
    credentials = db.relationship('Credentials', secondary=licenses_users_credentials, backref='licenses')
    
    # Relacionamento com Bots (conforme já definido antes)
    bots = db.relationship('BotsCrawJUD', secondary=licenses_users_bots, backref=db.backref('licenses', lazy=True))
    
    


