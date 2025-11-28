from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import ProjectService

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/projects', methods=['GET'])
@jwt_required()
def get_projects():
    """Pobieranie wszystkich projektów użytkownika"""
    try:
        current_user_id = get_jwt_identity()
        projects = ProjectService.get_user_projects(current_user_id)
        
        return jsonify({
            'projects': [p.to_dict() for p in projects]
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Błąd serwera: {str(e)}'}), 500


@projects_bp.route('/projects', methods=['POST'])
@jwt_required()
def create_project():
    """Tworzenie nowego projektu"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        result = ProjectService.create_project(
            user_id=current_user_id,
            name=data.get('name', ''),
            description=data.get('description', '')
        )
        
        return jsonify(result), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Błąd serwera: {str(e)}'}), 500


@projects_bp.route('/projects/<int:project_id>', methods=['GET'])
@jwt_required()
def get_project(project_id):
    """Pobieranie szczegółów projektu"""
    try:
        current_user_id = get_jwt_identity()
        project = ProjectService.get_project(project_id, current_user_id)
        
        return jsonify({'project': project.to_dict(include_members=True, include_tasks=True)}), 200
    
    except PermissionError as e:
        return jsonify({'error': str(e)}), 403
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Błąd serwera: {str(e)}'}), 500


@projects_bp.route('/projects/<int:project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id):
    """Aktualizacja projektu (tylko owner)"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        result = ProjectService.update_project(
            project_id=project_id,
            user_id=current_user_id,
            name=data.get('name'),
            description=data.get('description')
        )
        
        return jsonify(result), 200
    
    except PermissionError as e:
        return jsonify({'error': str(e)}), 403
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Błąd serwera: {str(e)}'}), 500


@projects_bp.route('/projects/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    """Usunięcie projektu (tylko owner)"""
    try:
        current_user_id = get_jwt_identity()
        ProjectService.delete_project(project_id, current_user_id)
        
        return jsonify({'message': 'Projekt usunięty pomyślnie'}), 200
    
    except PermissionError as e:
        return jsonify({'error': str(e)}), 403
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Błąd serwera: {str(e)}'}), 500


@projects_bp.route('/projects/<int:project_id>/invite', methods=['POST'])
@jwt_required()
def invite_user(project_id):
    """Dodanie użytkownika do projektu (tylko owner)"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        result = ProjectService.invite_user(
            project_id=project_id,
            owner_id=current_user_id,
            username=data.get('username', '')
        )
        
        return jsonify(result), 201
    
    except PermissionError as e:
        return jsonify({'error': str(e)}), 403
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Błąd serwera: {str(e)}'}), 500


@projects_bp.route('/projects/<int:project_id>/members/<int:member_user_id>', methods=['DELETE'])
@jwt_required()
def remove_member(project_id, member_user_id):
    """Usunięcie członka z projektu (tylko owner)"""
    try:
        current_user_id = get_jwt_identity()
        ProjectService.remove_member(
            project_id=project_id,
            owner_id=current_user_id,
            user_id=member_user_id
        )
        
        return jsonify({'message': 'Członek usunięty z projektu'}), 200
    
    except PermissionError as e:
        return jsonify({'error': str(e)}), 403
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Błąd serwera: {str(e)}'}), 500


