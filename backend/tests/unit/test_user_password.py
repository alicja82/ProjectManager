"""Unit test for User model password hashing"""
import pytest
from app.models import db, User


class TestUserPasswordHashing:
    """Test User model password hashing"""
    
    def test_password_hashing(self, app):
        """Test password is hashed correctly"""
        with app.app_context():
            user = User(username='testuser', email='test@test.com')
            user.set_password('mypassword')
            
            assert user.password_hash is not None
            assert user.password_hash != 'mypassword'
            assert user.check_password('mypassword') is True
            assert user.check_password('wrongpassword') is False
