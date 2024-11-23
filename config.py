import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///D:/test/database/site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.environ.get('DEBUG') == 'True' or False