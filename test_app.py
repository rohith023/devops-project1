"""
Test Suite for Drug Recommendation System
Tests the Flask REST API endpoints and basic functionality
"""
import pytest
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

@pytest.fixture
def client():
    """Create a test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

class TestHealthEndpoints:
    """Test health and info endpoints"""
    
    def test_home_endpoint(self, client):
        """Test home route"""
        response = client.get('/')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'message' in data
        assert 'version' in data
        assert 'timestamp' in data

    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'model_status' in data
        assert 'timestamp' in data

    def test_info_endpoint(self, client):
        """Test model info endpoint"""
        response = client.get('/info')
        # Should return either success or error based on model availability
        assert response.status_code in [200, 503]
        data = json.loads(response.data)
        assert 'status' in data

class TestPredictEndpoint:
    """Test prediction endpoint"""
    
    def test_predict_with_valid_input(self, client):
        """Test prediction with valid input"""
        # Only test if model is available
        response = client.get('/health')
        model_status = json.loads(response.data)['model_status']
        
        if model_status == 'not_loaded':
            pytest.skip("Model not loaded")
        
        payload = {
            'age': 45,
            'bp': 'HIGH',
            'cholesterol': 'NORMAL'
        }
        response = client.post('/predict',
                              data=json.dumps(payload),
                              content_type='application/json')
        assert response.status_code in [200, 503]
        data = json.loads(response.data)
        assert 'status' in data

    def test_predict_missing_fields(self, client):
        """Test prediction with missing required fields"""
        response = client.get('/health')
        model_status = json.loads(response.data)['model_status']
        
        if model_status == 'not_loaded':
            pytest.skip("Model not loaded")
        
        payload = {
            'age': 45,
            'bp': 'HIGH'
            # Missing cholesterol
        }
        response = client.post('/predict',
                              data=json.dumps(payload),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'

    def test_predict_invalid_age(self, client):
        """Test prediction with invalid age"""
        response = client.get('/health')
        model_status = json.loads(response.data)['model_status']
        
        if model_status == 'not_loaded':
            pytest.skip("Model not loaded")
        
        payload = {
            'age': -5,
            'bp': 'HIGH',
            'cholesterol': 'NORMAL'
        }
        response = client.post('/predict',
                              data=json.dumps(payload),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'

    def test_predict_invalid_bp(self, client):
        """Test prediction with invalid BP value"""
        response = client.get('/health')
        model_status = json.loads(response.data)['model_status']
        
        if model_status == 'not_loaded':
            pytest.skip("Model not loaded")
        
        payload = {
            'age': 45,
            'bp': 'INVALID',
            'cholesterol': 'NORMAL'
        }
        response = client.post('/predict',
                              data=json.dumps(payload),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'

    def test_predict_no_json(self, client):
        """Test prediction without JSON data"""
        response = client.get('/health')
        model_status = json.loads(response.data)['model_status']
        
        if model_status == 'not_loaded':
            pytest.skip("Model not loaded")
        
        response = client.post('/predict',
                              data='',
                              content_type='application/json')
        assert response.status_code == 400

class TestErrorHandling:
    """Test error handling"""
    
    def test_404_not_found(self, client):
        """Test 404 error handling"""
        response = client.get('/nonexistent')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['status'] == 'error'
        assert 'not found' in data['message'].lower()

    def test_predict_methods(self, client):
        """Test that /predict only accepts POST"""
        response = client.get('/predict')
        assert response.status_code == 405  # Method Not Allowed

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
