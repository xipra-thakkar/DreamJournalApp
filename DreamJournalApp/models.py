from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

class Note(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    note=db.Column(db.String(10000))
    date=db.Column(db.DateTime(timezone=True), default=func.now())
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(150))
    email=db.Column(db.String(150), unique=True)
    password=db.Column(db.String(150))
    notes=db.relationship('Note')
    
    def setPassword(self, password):
        self.password=generate_password_hash(password, method='sha256')
        
    def checkPassword(self, password):
        return check_password_hash(self.password, password)