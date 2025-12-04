from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import db, User
from sqlalchemy.exc import IntegrityError
import re

auth_bp = Blueprint('auth', __name__)

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    return len(password) >= 6

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not username or not email or not password:
            return jsonify({'error': 'Username, email i hasło są wymagane'}), 400
        
        if len(username) < 3:
            return jsonify({'error': 'Username musi mieć minimum 3 znaki'}), 400
        
        if not validate_email(email):
            return jsonify({'error': 'Nieprawidłowy format email'}), 400
        
        if not validate_password(password):
            return jsonify({'error': 'Hasło musi mieć minimum 6 znaków'}), 400
        
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Użytkownik o takiej nazwie już istnieje'}), 409
        
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email jest już zarejestrowany'}), 409
        
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'Rejestracja zakończona pomyślnie',
            'user': user.to_dict()
        }), 201
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Błąd podczas rejestracji - użytkownik już istnieje'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Błąd serwera: {str(e)}'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({'error': 'Username i hasło są wymagane'}), 400
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            return jsonify({'error': 'Nieprawidłowy username lub hasło'}), 401
        
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': 'Zalogowano pomyślnie',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Błąd serwera: {str(e)}'}), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Użytkownik nie został znaleziony'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': f'Błąd serwera: {str(e)}'}), 500
