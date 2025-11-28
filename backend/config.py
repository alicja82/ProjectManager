import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Konfiguracja aplikacji Flask"""
    
    # Klucze bezpieczeństwa - do zmiany na produkcji
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret-key-change-in-production')
    
    # Baza danych
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///projectmanager.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Token JWT ważny 24h
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    
    # CORS
    CORS_HEADERS = 'Content-Type'
