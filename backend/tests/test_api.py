"""
Comprehensive test suite for the BobaChain backend API.
Tests cover all endpoints, error handling, and validation.
"""

import pytest
import json
from flask import json as flask_json
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, validate_batch_creation_data, validate_batch_id, validate_tracking_step


@pytest.fixture
def client():
    """Fixture to provide a Flask test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_blockchain_service():
    """Fixture to provide a mock blockchain service."""
    with patch('app.blockchain_service') as mock:
        mock.is_connected.return_value = True
        yield mock


class TestValidationFunctions:
    """Tests for validation utility functions."""

    def test_validate_batch_creation_data_valid(self):
        """Test validation with valid batch data."""
        data = {"name": "Tapioca Pearls", "origin": "Taiwan"}
        is_valid, error = validate_batch_creation_data(data)
        assert is_valid is True
        assert error == ""

    def test_validate_batch_creation_data_missing_name(self):
        """Test validation with missing batch name."""
        data = {"origin": "Taiwan"}
        is_valid, error = validate_batch_creation_data(data)
        assert is_valid is False
        assert "name" in error.lower()

    def test_validate_batch_creation_data_missing_origin(self):
        """Test validation with missing batch origin."""
        data = {"name": "Tapioca Pearls"}
        is_valid, error = validate_batch_creation_data(data)
        assert is_valid is False
        assert "origin" in error.lower()

    def test_validate_batch_creation_data_empty_name(self):
        """Test validation with empty batch name."""
        data = {"name": "", "origin": "Taiwan"}
        is_valid, error = validate_batch_creation_data(data)
        assert is_valid is False

    def test_validate_batch_creation_data_name_too_long(self):
        """Test validation with batch name exceeding 255 characters."""
        data = {"name": "x" * 256, "origin": "Taiwan"}
        is_valid, error = validate_batch_creation_data(data)
        assert is_valid is False
        assert "255" in error

    def test_validate_batch_id_valid(self):
        """Test validation with valid batch ID."""
        is_valid, error = validate_batch_id("1")
        assert is_valid is True
        assert error == ""

    def test_validate_batch_id_zero(self):
        """Test validation with batch ID of 0."""
        is_valid, error = validate_batch_id("0")
        assert is_valid is False
        assert "positive" in error.lower()

    def test_validate_batch_id_negative(self):
        """Test validation with negative batch ID."""
        is_valid, error = validate_batch_id("-1")
        assert is_valid is False
        assert "positive" in error.lower()

    def test_validate_batch_id_non_integer(self):
        """Test validation with non-integer batch ID."""
        is_valid, error = validate_batch_id("abc")
        assert is_valid is False
        assert "integer" in error.lower()

    def test_validate_tracking_step_valid(self):
        """Test validation with valid tracking step."""
        is_valid, error = validate_tracking_step("Harvested")
        assert is_valid is True
        assert error == ""

    def test_validate_tracking_step_empty(self):
        """Test validation with empty tracking step."""
        is_valid, error = validate_tracking_step("")
        assert is_valid is False

    def test_validate_tracking_step_too_long(self):
        """Test validation with tracking step exceeding 255 characters."""
        is_valid, error = validate_tracking_step("x" * 256)
        assert is_valid is False
        assert "255" in error


class TestHealthCheck:
    """Tests for the health check endpoint."""

    def test_health_check_connected(self, client, mock_blockchain_service):
        """Test health check when blockchain is connected."""
        response = client.get('/api/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] in ['healthy', 'degraded']
        assert 'blockchain_connected' in data

    def test_health_check_disconnected(self, client):
        """Test health check when blockchain is not connected."""
        with patch('app.blockchain_service') as mock:
            mock.is_connected.return_value = False
            response = client.get('/api/health')
            assert response.status_code == 503


class TestCreateBatch:
    """Tests for the create batch endpoint."""

    def test_create_batch_success(self, client, mock_blockchain_service):
        """Test successful batch creation."""
        mock_blockchain_service.create_batch.return_value = "0x123abc"
        mock_blockchain_service.get_batch_count.return_value = 1

        response = client.post('/api/batch', json={
            "name": "Tapioca Pearls",
            "origin": "Taiwan"
        })

        assert response.status_code == 201
        data = response.get_json()
        assert data['message'] == "Batch created successfully"
        assert data['name'] == "Tapioca Pearls"
        assert data['origin'] == "Taiwan"
        assert 'tx_hash' in data

    def test_create_batch_missing_name(self, client, mock_blockchain_service):
        """Test batch creation with missing name."""
        response = client.post('/api/batch', json={
            "origin": "Taiwan"
        })

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'name' in data['error'].lower()

    def test_create_batch_missing_origin(self, client, mock_blockchain_service):
        """Test batch creation with missing origin."""
        response = client.post('/api/batch', json={
            "name": "Tapioca Pearls"
        })

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'origin' in data['error'].lower()

    def test_create_batch_no_json(self, client, mock_blockchain_service):
        """Test batch creation with no JSON body."""
        response = client.post('/api/batch')

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_create_batch_blockchain_error(self, client, mock_blockchain_service):
        """Test batch creation when blockchain call fails."""
        mock_blockchain_service.create_batch.return_value = None

        response = client.post('/api/batch', json={
            "name": "Tapioca Pearls",
            "origin": "Taiwan"
        })

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data

    def test_create_batch_blockchain_disconnected(self, client):
        """Test batch creation when blockchain is disconnected."""
        with patch('app.blockchain_service') as mock:
            mock.is_connected.return_value = False

            response = client.post('/api/batch', json={
                "name": "Tapioca Pearls",
                "origin": "Taiwan"
            })

            assert response.status_code == 503


class TestGetBatch:
    """Tests for the get batch endpoint."""

    def test_get_batch_success(self, client, mock_blockchain_service):
        """Test successful batch retrieval."""
        mock_blockchain_service.get_batch.return_value = {
            'id': 1,
            'name': 'Tapioca Pearls',
            'origin': 'Taiwan',
            'tracking_history': ['Harvested', 'Processed'],
            'timestamp': 1234567890
        }

        response = client.get('/api/batch/1')

        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == 1
        assert data['name'] == 'Tapioca Pearls'
        assert data['origin'] == 'Taiwan'

    def test_get_batch_not_found(self, client, mock_blockchain_service):
        """Test batch retrieval when batch doesn't exist."""
        mock_blockchain_service.get_batch.return_value = None

        response = client.get('/api/batch/999')

        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert 'not found' in data['error'].lower()

    def test_get_batch_invalid_id(self, client, mock_blockchain_service):
        """Test batch retrieval with invalid batch ID."""
        response = client.get('/api/batch/abc')

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'integer' in data['error'].lower()

    def test_get_batch_zero_id(self, client, mock_blockchain_service):
        """Test batch retrieval with batch ID of 0."""
        response = client.get('/api/batch/0')

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_get_batch_blockchain_disconnected(self, client):
        """Test batch retrieval when blockchain is disconnected."""
        with patch('app.blockchain_service') as mock:
            mock.is_connected.return_value = False

            response = client.get('/api/batch/1')

            assert response.status_code == 503


class TestAddTrackingStep:
    """Tests for the add tracking step endpoint."""

    def test_add_tracking_step_success(self, client, mock_blockchain_service):
        """Test successful tracking step addition."""
        mock_blockchain_service.add_tracking_step.return_value = "0x456def"

        response = client.post('/api/batch/1/tracking', json={
            "step": "Harvested"
        })

        assert response.status_code == 201
        data = response.get_json()
        assert data['message'] == "Tracking step added successfully"
        assert data['batch_id'] == '1'
        assert data['step'] == 'Harvested'
        assert 'tx_hash' in data

    def test_add_tracking_step_missing_step(self, client, mock_blockchain_service):
        """Test adding tracking step with missing step."""
        response = client.post('/api/batch/1/tracking', json={})

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_add_tracking_step_invalid_batch_id(self, client, mock_blockchain_service):
        """Test adding tracking step with invalid batch ID."""
        response = client.post('/api/batch/abc/tracking', json={
            "step": "Harvested"
        })

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_add_tracking_step_blockchain_error(self, client, mock_blockchain_service):
        """Test adding tracking step when blockchain call fails."""
        mock_blockchain_service.add_tracking_step.return_value = None

        response = client.post('/api/batch/1/tracking', json={
            "step": "Harvested"
        })

        assert response.status_code == 500


class TestGetAllBatches:
    """Tests for the get all batches endpoint."""

    def test_get_all_batches_success(self, client, mock_blockchain_service):
        """Test successful retrieval of all batches."""
        mock_blockchain_service.get_all_batches.return_value = [
            {
                'id': 1,
                'name': 'Tapioca Pearls',
                'origin': 'Taiwan',
                'tracking_history': ['Harvested'],
                'timestamp': 1234567890
            },
            {
                'id': 2,
                'name': 'Milk Tea',
                'origin': 'China',
                'tracking_history': ['Brewing'],
                'timestamp': 1234567891
            }
        ]

        response = client.get('/api/batches')

        assert response.status_code == 200
        data = response.get_json()
        assert data['count'] == 2
        assert len(data['batches']) == 2

    def test_get_all_batches_empty(self, client, mock_blockchain_service):
        """Test retrieval of all batches when none exist."""
        mock_blockchain_service.get_all_batches.return_value = []

        response = client.get('/api/batches')

        assert response.status_code == 200
        data = response.get_json()
        assert data['count'] == 0
        assert len(data['batches']) == 0

    def test_get_all_batches_blockchain_error(self, client, mock_blockchain_service):
        """Test retrieval of all batches when blockchain call fails."""
        mock_blockchain_service.get_all_batches.return_value = None

        response = client.get('/api/batches')

        assert response.status_code == 500


class TestSummary:
    """Tests for the summary endpoint."""

    def test_get_summary_success(self, client, mock_blockchain_service):
        """Test successful summary generation."""
        mock_blockchain_service.get_all_batches.return_value = [
            {
                'id': 1,
                'name': 'Tapioca Pearls',
                'origin': 'Taiwan',
                'tracking_history': ['Harvested', 'Processed'],
                'timestamp': 1234567890
            }
        ]

        response = client.get('/api/summary')

        assert response.status_code == 200
        data = response.get_json()
        assert 'summary' in data
        assert data['batch_count'] == 1
        assert 'Tapioca Pearls' in data['summary']

    def test_get_summary_empty_batches(self, client, mock_blockchain_service):
        """Test summary generation with no batches."""
        mock_blockchain_service.get_all_batches.return_value = []

        response = client.get('/api/summary')

        assert response.status_code == 200
        data = response.get_json()
        assert data['batch_count'] == 0


class TestErrorHandlers:
    """Tests for error handling."""

    def test_404_not_found(self, client):
        """Test 404 error handling."""
        response = client.get('/api/nonexistent')

        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data

    def test_405_method_not_allowed(self, client, mock_blockchain_service):
        """Test 405 error handling."""
        response = client.get('/api/batch', json={
            "name": "Test",
            "origin": "Test"
        })

        assert response.status_code == 405


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--cov=.', '--cov-report=html'])