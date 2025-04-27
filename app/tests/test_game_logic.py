import pytest
import json
from src.app import app, process_command

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def game_data():
    with open('src/game_data.json', 'r') as f:
        return json.load(f)

def test_home_endpoint(client):
    """Test the home endpoint returns correct welcome message"""
    response = client.get('/')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "Welcome to the New Zealand Adventure Game!" in data['message']
    assert "example_commands" in data
    assert len(data['example_commands']) > 0

def test_look_command():
    """Test the look command returns correct location information"""
    player_state = {
        'location': 'start',
        'inventory': [],
        'visited': ['start']
    }
    response = process_command('look', player_state)
    assert 'description' in response
    assert 'exits' in response
    assert 'items' in response
    assert 'Auckland Harbour' in response['description']
    assert 'map' in response['items']
    assert 'sunglasses' in response['items']

def test_take_command():
    """Test taking an item works correctly"""
    player_state = {
        'location': 'start',
        'inventory': [],
        'visited': ['start']
    }
    response = process_command('take map', player_state)
    assert 'message' in response
    assert response['message'] == 'You took the map.'
    assert 'map' in player_state['inventory']

def test_invalid_take():
    """Test taking a non-existent item"""
    player_state = {
        'location': 'start',
        'inventory': [],
        'visited': ['start']
    }
    response = process_command('take unicorn', player_state)
    assert 'error' in response
    assert response['error'] == 'There is no unicorn here.'

def test_inventory_command():
    """Test inventory command shows correct items"""
    player_state = {
        'location': 'start',
        'inventory': ['map', 'sunglasses'],
        'visited': ['start']
    }
    response = process_command('inventory', player_state)
    assert 'inventory' in response
    assert 'message' in response
    assert 'map' in response['inventory']
    assert 'sunglasses' in response['inventory']

def test_movement():
    """Test moving between locations"""
    player_state = {
        'location': 'start',
        'inventory': [],
        'visited': ['start']
    }
    response = process_command('go south', player_state)
    assert 'description' in response
    assert 'Sky Tower' in response['description']
    assert player_state['location'] == 'sky_tower'
    assert 'sky_tower' in player_state['visited']

def test_invalid_movement():
    """Test attempting to move in an invalid direction"""
    player_state = {
        'location': 'start',
        'inventory': [],
        'visited': ['start']
    }
    response = process_command('go north', player_state)
    assert 'error' in response
    assert "You can't go north from here." == response['error']

def test_invalid_command():
    """Test handling of invalid commands"""
    player_state = {
        'location': 'start',
        'inventory': [],
        'visited': ['start']
    }
    response = process_command('dance', player_state)
    assert 'error' in response
    assert response['error'] == "I don't understand that command." 