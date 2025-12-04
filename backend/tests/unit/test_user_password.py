"""Unit test for User model password hashing"""
import pytest
from app.models import db, User


class TestUserPasswordHashing:
    
    def test_password_hashing(self, app):
        with app.app_context():
            user = User(username='testuser', email='test@test.com')
            user.set_password('mypassword')
            
            assert user.password_hash is not None
            assert user.password_hash != 'mypassword'
            assert user.check_password('mypassword') is True
            assert user.check_password('wrongpassword') is False
