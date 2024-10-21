import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Naledi Neo'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///medapp.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False