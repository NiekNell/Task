from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """
    User table with function to incrypt/decrypt password
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        #incrypting
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        #decrypting
        return check_password_hash(self.password, password)

class File(db.Model):
    """
    File table
    """
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(255), nullable=False)
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Access(db.Model):
    """
    Access table - whitelist for users (if many users and files can lag. can optimise by give users tags and give acces by tags)
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('file_access', lazy=True))
    file = db.relationship('File', backref=db.backref('file_access', lazy=True))

class Log(db.Model):
    """
    Logs who what and when download
    """
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), nullable=True)
    user = db.relationship('User', backref=db.backref('logs', lazy=True))
    file = db.relationship('File', backref=db.backref('logs', lazy=True))
