"""Models package - exports all models and database instance"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.models.user import User
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.task import Task

__all__ = ['db', 'User', 'Project', 'ProjectMember', 'Task']
