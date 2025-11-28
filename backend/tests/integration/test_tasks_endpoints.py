"""Integration test for tasks endpoints"""
import pytest


class TestTasksEndpoints:
    """Integration test for tasks"""
    
    def test_list_project_tasks(self, client, auth_headers, sample_project):
        """Test listing tasks for a project"""
        response = client.get(
            f'/api/projects/{sample_project.id}/tasks',
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.get_json()
        assert 'tasks' in data
        assert isinstance(data['tasks'], list)
