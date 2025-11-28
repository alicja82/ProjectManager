"""Authentication service - business logic for user authentication"""
from app.models import db, User
from flask_jwt_extended import create_access_token


class AuthService:
    """Service handling authentication logic"""
    
    @staticmethod
    def register_user(username: str, email: str, password: str) -> dict:
        """Register a new user"""
        if not username or not email or not password:
            raise ValueError('Wszystkie pola są wymagane')
        
        if len(password) < 6:
            raise ValueError('Hasło musi mieć co najmniej 6 znaków')
        
        if User.query.filter_by(username=username).first():
            raise ValueError('Użytkownik o takiej nazwie już istnieje')
        
        if User.query.filter_by(email=email).first():
            raise ValueError('Użytkownik o takim emailu już istnieje')
        
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return {
            'message': 'Użytkownik zarejestrowany pomyślnie',
            'user': user.to_dict()
        }
    
    @staticmethod
    def login_user(username: str, password: str) -> dict:
        """Login user and generate JWT token"""
        if not username or not password:
            raise ValueError('Username i hasło są wymagane')
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            raise ValueError('Nieprawidłowe dane logowania')
        
        access_token = create_access_token(identity=user.id)
        
        return {
            'access_token': access_token,
            'user': user.to_dict()
        }
