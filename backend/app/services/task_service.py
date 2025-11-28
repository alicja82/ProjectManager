"""Task service - business logic for task management"""
from app.models import db, Task, Project, ProjectMember
from typing import List, Optional


class TaskService:
    """Service handling task-related business logic"""
    
    @staticmethod
    def get_project_tasks(project_id: int, user_id: int, status: Optional[str] = None, assigned_to: Optional[int] = None) -> List[Task]:
        """Get all tasks for a project with optional filtering"""
        project = Project.query.get(project_id)
        if not project:
            raise ValueError('Projekt nie został znaleziony')
        
        is_member = ProjectMember.query.filter_by(user_id=user_id, project_id=project_id).first()
        if not is_member and project.owner_id != user_id:
            raise PermissionError('Brak dostępu do tego projektu')
        
        query = Task.query.filter_by(project_id=project_id)
        
        if status:
            query = query.filter_by(status=status)
        
        if assigned_to:
            query = query.filter_by(assigned_to=assigned_to)
        
        return query.order_by(Task.created_at.desc()).all()
    
    @staticmethod
    def create_task(project_id: int, user_id: int, title: str, description: str = '', status: str = 'To do', assigned_to: Optional[int] = None) -> dict:
        """Create a new task"""
        project = Project.query.get(project_id)
        if not project:
            raise ValueError('Projekt nie został znaleziony')
        
        is_member = ProjectMember.query.filter_by(user_id=user_id, project_id=project_id).first()
        if not is_member and project.owner_id != user_id:
            raise PermissionError('Brak dostępu do tego projektu')
        
        if not title or not title.strip():
            raise ValueError('Tytuł zadania jest wymagany')
        
        valid_statuses = ['To do', 'In progress', 'Done']
        if status not in valid_statuses:
            raise ValueError(f'Status musi być jednym z: {", ".join(valid_statuses)}')
        
        # Weryfikacja czy assigned_to jest członkiem projektu (bezpieczeństwo)
        if assigned_to:
            assigned_member = ProjectMember.query.filter_by(user_id=assigned_to, project_id=project_id).first()
            if not assigned_member:
                raise ValueError('Nie można przypisać zadania do użytkownika spoza projektu')
        
        task = Task(title=title.strip(), description=description.strip(), project_id=project_id, assigned_to=assigned_to, status=status)
        db.session.add(task)
        db.session.commit()
        
        return {'message': 'Zadanie utworzone pomyślnie', 'task': task.to_dict()}
    
    @staticmethod
    def update_task(task_id: int, user_id: int, title: Optional[str] = None, description: Optional[str] = None, status: Optional[str] = None, assigned_to: Optional[int] = None) -> dict:
        """Update a task"""
        task = Task.query.get(task_id)
        if not task:
            raise ValueError('Zadanie nie zostało znalezione')
        
        is_member = ProjectMember.query.filter_by(user_id=user_id, project_id=task.project_id).first()
        if not is_member and task.project.owner_id != user_id:
            raise PermissionError('Brak dostępu do tego zadania')
        
        if title is not None:
            title = title.strip()
            if not title:
                raise ValueError('Tytuł zadania nie może być pusty')
            task.title = title
        
        if description is not None:
            task.description = description.strip()
        
        if status is not None:
            valid_statuses = ['To do', 'In progress', 'Done']
            if status not in valid_statuses:
                raise ValueError(f'Status musi być jednym z: {", ".join(valid_statuses)}')
            task.status = status
        
        # assigned_to > 0 oznacza przypisanie, <= 0 oznacza odznaczenie przypisania
        if assigned_to is not None:
            if assigned_to > 0:
                assigned_member = ProjectMember.query.filter_by(user_id=assigned_to, project_id=task.project_id).first()
                if not assigned_member:
                    raise ValueError('Nie można przypisać zadania do użytkownika spoza projektu')
                task.assigned_to = assigned_to
            else:
                task.assigned_to = None
        
        db.session.commit()
        return {'message': 'Zadanie zaktualizowane pomyślnie', 'task': task.to_dict()}
    
    @staticmethod
    def delete_task(task_id: int, user_id: int) -> dict:
        """Delete a task"""
        task = Task.query.get(task_id)
        if not task:
            raise ValueError('Zadanie nie zostało znalezione')
        
        is_member = ProjectMember.query.filter_by(user_id=user_id, project_id=task.project_id).first()
        if not is_member and task.project.owner_id != user_id:
            raise PermissionError('Brak dostępu do tego zadania')
        
        db.session.delete(task)
        db.session.commit()
        return {'message': 'Zadanie usunięte pomyślnie'}
