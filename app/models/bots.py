from app import db

class BotsCrawJUD(db.Model):
    
    __tablename__ = 'bots'
    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(length=45), nullable=False)
    system = db.Column(db.String(length=45), nullable=False)
    state = db.Column(db.String(length=45), nullable=False)
    client = db.Column(db.String(length=45), nullable=False)
    type = db.Column(db.String(length=45), nullable=False)
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
    
