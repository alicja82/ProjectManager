"""User model"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacje z cascade delete - usunięcie usera usuwa jego członkostwa w projektach
    owned_projects = db.relationship('Project', backref='owner', lazy=True, foreign_keys='Project.owner_id')
    project_memberships = db.relationship('ProjectMember', backref='user', lazy=True, cascade='all, delete-orphan')
    assigned_tasks = db.relationship('Task', backref='assigned_user', lazy=True, foreign_keys='Task.assigned_to')
    
    def set_password(self, password):
        """Hashuje hasło przez werkzeug.security (bcrypt)"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Weryfikuje hasło wobec zapisanego hasha"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }
