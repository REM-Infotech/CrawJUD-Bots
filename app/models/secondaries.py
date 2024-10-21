from app import db


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

execution_licenses = db.Table(
    'execution_licenses',
    db.Column('executions_id', db.Integer, db.ForeignKey('executions.id'), primary_key=True),
    db.Column('licenses_users_id', db.Integer, db.ForeignKey('licenses_users.id'), primary_key=True)
)