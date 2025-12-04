"""Unit test for Task model creation"""
import pytest
from app.models import db, User, Project, Task


class TestTaskCreation:
    
    def test_task_creation(self, app):
        with app.app_context():
            user = User(username='user', email='user@test.com')
            user.set_password('password')
            db.session.add(user)
            db.session.flush()
            
            project = Project(name='Project', owner_id=user.id)
            db.session.add(project)
            db.session.flush()
            
            task = Task(
                title='My Task',
                description='Task description',
                project_id=project.id,
                status='To Do'
            )
            db.session.add(task)
            db.session.commit()
            
            assert task.id is not None
            assert task.title == 'My Task'
            assert task.status == 'To Do'
