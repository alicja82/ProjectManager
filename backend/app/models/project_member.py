"""ProjectMember model"""
from datetime import datetime
from app.models import db


class ProjectMember(db.Model):
    __tablename__ = 'project_members'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='member')  # owner, member
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint - jeden użytkownik nie może być dwukrotnie w tym samym projekcie
    __table_args__ = (db.UniqueConstraint('user_id', 'project_id', name='_user_project_uc'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user.to_dict() if self.user else None,
            'project_id': self.project_id,
            'role': self.role,
            'joined_at': self.joined_at.isoformat()
        }
