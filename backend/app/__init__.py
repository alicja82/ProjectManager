from flask import Flask, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from app.models import db

jwt = JWTManager()

def create_app(config_class=Config):
    """Factory pattern - umożliwia różne konfiguracje (dev, test, prod)"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicjalizacja rozszerzeń
    db.init_app(app)
    CORS(app)
    jwt.init_app(app)
    
    # Rejestracja blueprintów (routes)
    from app.routes.auth import auth_bp
    from app.routes.projects import projects_bp
    from app.routes.tasks import tasks_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(projects_bp, url_prefix='/api')
    app.register_blueprint(tasks_bp, url_prefix='/api')
    
    # JWT Error Handlers
    from flask import jsonify
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token wygasł'}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'error': 'Nieprawidłowy token'}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({'error': 'Brak tokenu autoryzacji'}), 401
    
    # Auto-tworzenie tabel - tylko dev! W produkcji użyj Flask-Migrate
    with app.app_context():
        db.create_all()
    
    return app
