"""Pytest configuration and fixtures"""
import pytest
from app import create_app
from app.models import db, User, Project, ProjectMember, Task
from config import Config


class TestConfig(Config):
    """Test configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory database for tests
    WTF_CSRF_ENABLED = False
    JWT_SECRET_KEY = 'test-secret-key'


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app(TestConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def sample_user(app):
    """Create a sample user for testing"""
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        user_id = user.id
    
    # Return a fresh instance from the database
    with app.app_context():
        return db.session.get(User, user_id)


@pytest.fixture
def sample_user2(app):
    """Create a second sample user for testing"""
    with app.app_context():
        user = User(username='testuser2', email='test2@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        user_id = user.id
    
    # Return a fresh instance from the database
    with app.app_context():
        return db.session.get(User, user_id)


@pytest.fixture
def sample_project(app, sample_user):
    """Create a sample project for testing"""
    with app.app_context():
        # Get fresh user instance in this context
        user = db.session.get(User, sample_user.id)
        
        project = Project(
            name='Test Project',
            description='Test Description',
            owner_id=user.id
        )
        db.session.add(project)
        db.session.flush()
        
        # Add owner as member
        member = ProjectMember(
            user_id=user.id,
            project_id=project.id,
            role='owner'
        )
        db.session.add(member)
        db.session.commit()
        project_id = project.id
    
    # Return a fresh instance from the database
    with app.app_context():
        return db.session.get(Project, project_id)


@pytest.fixture
def auth_headers(client, sample_user):
    """Get authentication headers with JWT token"""
    response = client.post('/api/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    token = response.get_json()['access_token']
    return {'Authorization': f'Bearer {token}'}
