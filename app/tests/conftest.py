import os
import pytest
from google.cloud import firestore
from app.src.app import app

@pytest.fixture(autouse=True)
def setup_test_env():
    """Setup test environment variables before each test"""
    os.environ['FIRESTORE_EMULATOR_HOST'] = 'localhost:8081'
    yield
    # Clean up
    if 'FIRESTORE_EMULATOR_HOST' in os.environ:
        del os.environ['FIRESTORE_EMULATOR_HOST']

@pytest.fixture
def client():
    """Test client for Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def firestore_client():
    """Create a Firestore client connected to the emulator"""
    return firestore.Client(project='test-project') 