"""Integration test for authentication flow"""
import pytest


class TestAuthFlow:
    """Integration test for authentication"""
    
    def test_register_login_flow(self, client):
        """Test complete registration and login flow"""
        # Step 1: Register a new user
        register_response = client.post('/api/register', json={
            'username': 'integrationuser',
            'email': 'integration@example.com',
            'password': 'secure123'
        })
        
        assert register_response.status_code == 201
        register_data = register_response.get_json()
        assert register_data['user']['username'] == 'integrationuser'
        assert register_data['user']['email'] == 'integration@example.com'
        
        # Step 2: Login with the registered credentials
        login_response = client.post('/api/login', json={
            'username': 'integrationuser',
            'password': 'secure123'
        })
        
        assert login_response.status_code == 200
        login_data = login_response.get_json()
        assert 'access_token' in login_data
        assert login_data['user']['username'] == 'integrationuser'
        
        # Step 3: Verify the token can be used for authenticated requests
        token = login_data['access_token']
        projects_response = client.get(
            '/api/projects',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert projects_response.status_code == 200
