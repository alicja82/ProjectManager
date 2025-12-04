"""Integration tests for task endpoints."""

import pytest


class TestTasksEndpoints:

    def test_list_project_tasks(self, client, auth_headers, sample_project):

        response = client.get(
            f"/api/projects/{sample_project.id}/tasks",
            headers=auth_headers
        )

        assert response.status_code == 200

        data = response.get_json()

        assert isinstance(data, dict), "Response should be a JSON object"
        assert "tasks" in data, "Response should contain 'tasks' key"
        assert isinstance(data["tasks"], list), "'tasks' should be a list"

        if data["tasks"]:
            first = data["tasks"][0]
            assert isinstance(first, dict), "Each task should be a JSON object"
            assert "id" in first
            assert "title" in first
            assert "status" in first
