import pytest
import json
from app.src.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_missing_command(client):
    response = client.post('/game', json={})
    assert response.status_code == 400
    assert json.loads(response.data)['error'] == 'No command provided'

def test_look_command(client, firestore_client):
    # Initialize player state in emulator
    player_ref = firestore_client.collection('players').document('test_player')
    player_ref.set({
        'location': 'start',
        'inventory': [],
        'visited': ['start']
    })

    response = client.post('/game', json={
        'command': 'look',
        'player_id': 'test_player'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'description' in data
    assert 'exits' in data
    assert 'items' in data

def test_movement_command(client, firestore_client):
    # Initialize player state
    player_ref = firestore_client.collection('players').document('test_movement_player')
    player_ref.set({
        'location': 'start',
        'inventory': [],
        'visited': ['start']
    })

    # Try to move in a valid direction
    response = client.post('/game', json={
        'command': 'go south',
        'player_id': 'test_movement_player'
    })
    assert response.status_code == 200
    
    # Verify state was updated
    updated_state = player_ref.get().to_dict()
    assert updated_state['location'] == 'sky_tower'
    assert 'sky_tower' in updated_state['visited']

def test_inventory_command(client, firestore_client):
    # Initialize player state with some items
    player_ref = firestore_client.collection('players').document('test_inventory_player')
    player_ref.set({
        'location': 'start',
        'inventory': ['map', 'sunglasses'],
        'visited': ['start']
    })

    response = client.post('/game', json={
        'command': 'inventory',
        'player_id': 'test_inventory_player'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'inventory' in data
    assert isinstance(data['inventory'], list)
    assert 'map' in data['inventory']
    assert 'sunglasses' in data['inventory']

def test_take_command(client, firestore_client):
    # Initialize player state
    player_ref = firestore_client.collection('players').document('test_take_player')
    player_ref.set({
        'location': 'start',
        'inventory': [],
        'visited': ['start']
    })
    
    response = client.post('/game', json={
        'command': 'take map',
        'player_id': 'test_take_player'
    })
    assert response.status_code == 200
    
    # Verify item was added to inventory
    updated_state = player_ref.get().to_dict()
    assert 'map' in updated_state['inventory']

def test_invalid_command(client, firestore_client):
    # Initialize player state
    player_ref = firestore_client.collection('players').document('test_invalid_player')
    player_ref.set({
        'location': 'start',
        'inventory': [],
        'visited': ['start']
    })

    response = client.post('/game', json={
        'command': 'invalid',
        'player_id': 'test_invalid_player'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == "I don't understand that command." 