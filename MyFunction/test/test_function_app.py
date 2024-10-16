import pytest
from unittest.mock import patch, MagicMock
import azure.functions as func
import json
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file for testing
load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from function_app import http_triggersheri

@pytest.fixture
def mock_request():
    req = MagicMock(spec=func.HttpRequest)
    req.params = {}
    req.get_json.return_value = {}
    return req

@patch('function_app.container')
def http_triggersheri_with_name(mock_container, mock_request, monkeypatch):
    # Load environment variables for testing
    monkeypatch.setenv("COSMOS_DB_ENDPOINT", os.getenv("COSMOS_DB_ENDPOINT"))
    monkeypatch.setenv("COSMOS_DB_KEY", os.getenv("COSMOS_DB_KEY"))

    # Set up the mock return value for the container's read_item method
    mock_container.read_item.return_value = {'visitor_count': 1}

    # Simulate a request with a name
    mock_request.get_json.return_value = {'name': 'Sheri'}

    response = http_triggersheri(mock_request)

    assert response.status_code == 200
    data = json.loads(response.get_body())
    assert data['message'] == "Hello, Sheri. Your name has been added to the database."
    assert data['visitor_count'] == 1


@patch('function_app.container')
def test_http_triggersheri_without_name(mock_container, mock_request):
    # Set up the mock return value for the container's read_item method
    mock_container.read_item.return_value = {'visitor_count': 1}

    response = http_triggersheri(mock_request)
    
    assert response.status_code == 200
    data = json.loads(response.get_body())
    assert data['message'] == "This HTTP triggered function executed successfully."
    assert data['visitor_count'] == 1
