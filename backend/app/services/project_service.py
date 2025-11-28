"""Project service - business logic for project management"""
from app.models import db, Project, ProjectMember, User
from typing import List, Optional


class ProjectService:
    """Service handling project-related business logic"""
    
    @staticmethod
    def get_user_projects(user_id: int) -> List[Project]:
        """Get all projects for a user (owned + member)"""
        owned_projects = Project.query.filter_by(owner_id=user_id).all()
        memberships = ProjectMember.query.filter_by(user_id=user_id).all()
        # Filtrowanie projektów gdzie user jest członkiem ale nie ownerem (aby uniknąć duplikatów)
        member_projects = [m.project for m in memberships if m.project.owner_id != user_id]
        return owned_projects + member_projects
    
    @staticmethod
    def create_project(user_id: int, name: str, description: str = '') -> dict:
        """Create a new project"""
        try:
            name = name.strip() if name else ''
            description = description.strip() if description else ''
            
            if not name:
                raise ValueError('Nazwa projektu jest wymagana')
            
            project = Project(name=name, description=description, owner_id=user_id)
            db.session.add(project)
            db.session.flush()  # Potrzebne project.id przed utworzeniem ProjectMember
            
            owner_member = ProjectMember(user_id=user_id, project_id=project.id, role='owner')
            db.session.add(owner_member)
            db.session.commit()
            
            return {
                'message': 'Projekt utworzony pomyślnie',
                'project': project.to_dict(include_members=True)
            }
        except Exception as e:
            db.session.rollback()
            raise
    
    @staticmethod
    def get_project(project_id: int, user_id: int) -> Project:
        """Get project details with access check"""
        project = Project.query.get(project_id)
        if not project:
            raise ValueError('Projekt nie został znaleziony')
        
        is_member = ProjectMember.query.filter_by(user_id=user_id, project_id=project_id).first()
        if not is_member and project.owner_id != user_id:
            raise PermissionError('Brak dostępu do tego projektu')
        
        return project
    
    @staticmethod
    def update_project(project_id: int, user_id: int, name: Optional[str] = None, description: Optional[str] = None) -> dict:
        """Update project (owner only)"""
        project = Project.query.get(project_id)
        if not project:
            raise ValueError('Projekt nie został znaleziony')
        
        if project.owner_id != user_id:
            raise PermissionError('Tylko właściciel może edytować projekt')
        
        if name is not None:
            name = name.strip()
            if not name:
                raise ValueError('Nazwa projektu nie może być pusta')
            project.name = name
        
        if description is not None:
            project.description = description.strip()
        
        db.session.commit()
        return {'message': 'Projekt zaktualizowany pomyślnie', 'project': project.to_dict()}
    
    @staticmethod
    def delete_project(project_id: int, user_id: int) -> dict:
        """Delete project (owner only)"""
        project = Project.query.get(project_id)
        if not project:
            raise ValueError('Projekt nie został znaleziony')
        
        if project.owner_id != user_id:
            raise PermissionError('Tylko właściciel może usunąć projekt')
        
        db.session.delete(project)
        db.session.commit()
        return {'message': 'Projekt usunięty pomyślnie'}
    
    @staticmethod
    def invite_user(project_id: int, owner_id: int, username: str) -> dict:
        """Invite user to project (owner only)"""
        project = Project.query.get(project_id)
        if not project:
            raise ValueError('Projekt nie został znaleziony')
        
        if project.owner_id != owner_id:
            raise PermissionError('Tylko właściciel może dodawać członków')
        
        if not username or not username.strip():
            raise ValueError('Username jest wymagany')
        
        user = User.query.filter_by(username=username.strip()).first()
        if not user:
            raise ValueError('Użytkownik nie został znaleziony')
        
        existing_member = ProjectMember.query.filter_by(user_id=user.id, project_id=project_id).first()
        if existing_member:
            raise ValueError('Użytkownik jest już członkiem projektu')
        
        member = ProjectMember(user_id=user.id, project_id=project_id, role='member')
        db.session.add(member)
        db.session.commit()
        
        return {'message': f'Użytkownik {username} został dodany do projektu', 'member': member.to_dict()}
    
    @staticmethod
    def remove_member(project_id: int, owner_id: int, user_id: int) -> dict:
        """Remove member from project (owner only)"""
        project = Project.query.get(project_id)
        if not project:
            raise ValueError('Projekt nie został znaleziony')
        
        if project.owner_id != owner_id:
            raise PermissionError('Tylko właściciel może usuwać członków')
        
        if user_id == owner_id:
            raise ValueError('Nie możesz usunąć siebie z projektu')
        
        member = ProjectMember.query.filter_by(user_id=user_id, project_id=project_id).first()
        if not member:
            raise ValueError('Członek nie został znaleziony')
        
        db.session.delete(member)
        db.session.commit()
        return {'message': 'Członek usunięty z projektu'}
