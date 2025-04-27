from flask import Flask, request, jsonify
from google.cloud import firestore
import os
import json

app = Flask(__name__)
db = firestore.Client()

# Load game data
with open('game_data.json', 'r') as f:
    GAME_DATA = json.load(f)

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the New Zealand Adventure Game!",
        "instructions": "Send POST requests to /game with your commands.",
        "example_commands": ["look", "inventory", "go north", "take item"]
    })

@app.route('/game', methods=['POST'])
def game():
    data = request.get_json()
    if not data or 'command' not in data:
        return jsonify({"error": "No command provided"}), 400
    
    command = data['command'].lower()
    player_id = data.get('player_id', 'default')
    
    # Get player state from Firestore
    player_ref = db.collection('players').document(player_id)
    player_doc = player_ref.get()
    
    if not player_doc.exists:
        # Initialize new player
        player_state = {
            'location': 'start',
            'inventory': [],
            'visited': ['start']
        }
        player_ref.set(player_state)
    else:
        player_state = player_doc.to_dict()
    
    # Process command
    response = process_command(command, player_state)
    
    # Update player state
    player_ref.update(player_state)
    
    return jsonify(response)

def process_command(command, player_state):
    location = player_state['location']
    current_room = GAME_DATA['locations'][location]
    
    if command == 'look':
        return {
            "description": current_room['description'],
            "exits": current_room['exits'],
            "items": current_room.get('items', [])
        }
    
    if command.startswith('go '):
        direction = command[3:]
        if direction in current_room['exits']:
            new_location = current_room['exits'][direction]
            player_state['location'] = new_location
            if new_location not in player_state['visited']:
                player_state['visited'].append(new_location)
            return process_command('look', player_state)
        return {"error": f"You can't go {direction} from here."}
    
    if command.startswith('take '):
        item = command[5:]
        if item in current_room.get('items', []):
            current_room['items'].remove(item)
            player_state['inventory'].append(item)
            return {"message": f"You took the {item}."}
        return {"error": f"There is no {item} here."}
    
    if command == 'inventory':
        return {
            "inventory": player_state['inventory'],
            "message": "You are carrying:" if player_state['inventory'] else "You are not carrying anything."
        }
    
    return {"error": "I don't understand that command."}

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port) 