# Configuration settings for Flask
import os

class Config:
    """Base configuration class."""
    
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'CureMedFindme'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable track modifications to save memory

    # Other configurations 
    DEBUG = os.environ.get('DEBUG', 'True') == 'True'  
    JSON_SORT_KEYS = False  # Prevent sorting of JSON keys in responses
