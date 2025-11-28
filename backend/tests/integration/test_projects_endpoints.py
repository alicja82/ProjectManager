"""Integration test for projects endpoints"""
import pytest


class TestProjectsEndpoints:
    """Integration test for projects"""
    
    def test_create_and_list_projects(self, client, auth_headers):
        """Test creating a project and listing all projects"""
        # Create a project
        response = client.post('/api/projects',
            headers=auth_headers,
            json={'name': 'Test Project', 'description': 'Test Description'}
        )
        assert response.status_code == 201
        data = response.get_json()
        assert 'project' in data
        assert data['project']['name'] == 'Test Project'
        
        # List all projects
        response = client.get('/api/projects', headers=auth_headers)
        assert response.status_code == 200
        projects = response.get_json()['projects']
        assert len(projects) >= 1
        assert any(p['name'] == 'Test Project' for p in projects)
