from app import db

import pytz
from datetime import datetime

execution_bots = db.Table(
    'execution_bots',
    db.Column('execution_id', db.Integer, db.ForeignKey('executions.id'), primary_key=True),
    db.Column('bot_id', db.Integer, db.ForeignKey('bots.id'), primary_key=True)
)

# Tabela de associação para LicensesUsers e Credentials
execution_users = db.Table(
    'execution_users',
    db.Column('executions_id', db.Integer, db.ForeignKey('executions.id'), primary_key=True),
    db.Column('users_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

class BotsCrawJUD(db.Model):
    
    __tablename__ = 'bots'
    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(length=45), nullable=False)
    system = db.Column(db.String(length=45), nullable=False)
    state = db.Column(db.String(length=45), nullable=False)
    client = db.Column(db.String(length=45), nullable=False)
    type = db.Column(db.String(length=45), nullable=False)
    form_cfg = db.Column(db.String(length=45), nullable=False)
    classification = db.Column(db.String(length=45), nullable=False)
    text = db.Column(db.String(length=512), nullable=False)
    
class Credentials(db.Model):
    
    __tablename__ = 'credentials'
    id = db.Column(db.Integer, primary_key=True)
    nome_credencial = db.Column(db.String(length=45), nullable=False)
    system = db.Column(db.String(length=45), nullable=False)
    login_method = db.Column(db.String(length=45), nullable=False)
    login = db.Column(db.String(length=45), nullable=False)
    password = db.Column(db.String(length=45))
    key = db.Column(db.String(length=45))
    certficate = db.Column(db.String(length=45))
    certficate_blob = db.Column(db.LargeBinary(length=(2**32)-1))
    
class Executions(db.Model):
    
    __tablename__ = 'executions'
    pid = db.Column(db.String(length=12), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(length=50), nullable=False)
    status = db.Column(db.String(length=45), nullable=False)
    file_output = db.Column(db.String(length=512))
    total_rows = db.Column(db.String(length=45))
    url_socket = db.Column(db.String(length=64))
    data_execucao = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Etc/GMT+4')))
    data_finalizacao = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Etc/GMT+4')))
    arquivo_xlsx = db.Column(db.String(length=64))

    # Relacionamento com Bots (conforme já definido antes)
    bot = db.relationship('BotsCrawJUD', secondary=execution_bots, backref=db.backref('executions', lazy=True))
    user = db.relationship('Users', secondary=execution_users, backref=db.backref('executions', lazy=True))
