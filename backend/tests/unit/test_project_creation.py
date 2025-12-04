"""Unit test for Project model creation"""
import pytest
from app.models import db, User, Project


class TestProjectCreation:
    
    def test_project_creation(self, app):
        with app.app_context():
            user = User(username='owner', email='owner@test.com')
            user.set_password('password')
            db.session.add(user)
            db.session.flush()
            
            project = Project(
                name='Test Project',
                description='Description',
                owner_id=user.id
            )
            db.session.add(project)
            db.session.commit()
            
            assert project.id is not None
            assert project.name == 'Test Project'
            assert project.owner_id == user.id
