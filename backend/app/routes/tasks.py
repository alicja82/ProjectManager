from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import TaskService

tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('/projects/<int:project_id>/tasks', methods=['GET'])
@jwt_required()
def get_tasks(project_id):
    """Pobieranie wszystkich zadań projektu z opcjonalnym filtrowaniem"""
    try:
        current_user_id = get_jwt_identity()
        status = request.args.get('status')
        assigned_to = request.args.get('assigned_to')
        
        tasks = TaskService.get_project_tasks(
            project_id=project_id,
            user_id=current_user_id,
            status=status,
            assigned_to=int(assigned_to) if assigned_to else None
        )
        
        return jsonify({'tasks': [t.to_dict() for t in tasks]}), 200
        
    except PermissionError as e:
        return jsonify({'error': str(e)}), 403
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Błąd serwera: {str(e)}'}), 500


@tasks_bp.route('/projects/<int:project_id>/tasks', methods=['POST'])
@jwt_required()
def create_task(project_id):
    """Tworzenie nowego zadania w projekcie"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        result = TaskService.create_task(
            project_id=project_id,
            user_id=current_user_id,
            title=data.get('title', ''),
            description=data.get('description', ''),
            status=data.get('status', 'To do'),
            assigned_to=data.get('assigned_to')
        )
        
        return jsonify(result), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Błąd serwera: {str(e)}'}), 500


@tasks_bp.route('/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    """Pobieranie szczegółów zadania"""
    try:
        current_user_id = get_jwt_identity()
        task = TaskService.get_task(current_user_id, task_id)
        
        return jsonify({'task': task.to_dict()}), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Błąd serwera: {str(e)}'}), 500


@tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    """Aktualizacja zadania"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        result = TaskService.update_task(
            task_id=task_id,
            user_id=current_user_id,
            title=data.get('title'),
            description=data.get('description'),
            status=data.get('status'),
            assigned_to=data.get('assigned_to')
        )
        
        return jsonify(result), 200
    
    except PermissionError as e:
        return jsonify({'error': str(e)}), 403
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Błąd serwera: {str(e)}'}), 500


@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """Usunięcie zadania"""
    try:
        current_user_id = get_jwt_identity()
        TaskService.delete_task(task_id, current_user_id)
        
        return jsonify({'message': 'Zadanie usunięte pomyślnie'}), 200
    
    except PermissionError as e:
        return jsonify({'error': str(e)}), 403
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Błąd serwera: {str(e)}'}), 500
