# FILE: main.py
import json
from flask import Flask, request, jsonify
from routes import bp as routes_bp
import sys
sys.setdefaultencoding("UTF-16")

app = Flask(__name__)
app.register_blueprint(routes_bp)

def load_planets():
    with open('planets.json', 'r') as file:
        return json.load(file)

def load_players():
    with open('players.json', 'r') as file:
        return json.load(file)

def save_players(players):
    with open('players.json', 'w') as file:
        json.dump(players, file, indent=4)

@app.route('/planet', methods=['GET'])
def get_planet():
    planet_id = request.args.get('planetId')
    planets = load_planets()
    for planet in planets:
        if planet['planetId'] == planet_id:
            return jsonify(planet)
    return jsonify({"error": "Planet not found"}), 404

@app.route('/move', methods=['POST'])
def move_to_planet():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    player_id = data.get('player_id')
    destination_planet_id = data.get('destination_planet_id')
    
    # Load data
    players = load_players()
    planets = load_planets()
    
    # Find player and planet
    player = None
    destination_planet = None
    
    for p in players:
        if p['playerId'] == player_id:
            player = p
            break
    
    for p in planets:
        if p['planetId'] == destination_planet_id:
            destination_planet = p
            break
    
    if not player or not destination_planet:
        return jsonify({
            "error": "Spieler oder Planet nicht gefunden",
            "message": "Bewegung nicht möglich"
        }), 404
    
    # Check if player has enough fuel
    if player['inventory']['fuel'] < 10:
        return jsonify({
            "error": "Nicht genug Treibstoff",
            "message": "Mindestens 10 Treibstoffeinheiten benötigt"
        }), 400
    
    # Update player's fuel and current planet
    player['inventory']['fuel'] -= 10
    player['currentPlanetId'] = destination_planet_id
    
    # Save updated player data
    save_players(players)
    
    # Prepare response
    response = {
        "player": player,
        "planet": destination_planet,
        "message": f"Du bist zu einem neuen Planeten gereist:\n\t→ {destination_planet['name']}. Treibstoffverbrauch: 10 Einheiten."
    }
    
    return jsonify(response)

def main():
    print("Willkommen bei Space Explorer, dem Spiel in deiner Konsole!")
    app.run(debug=True)

if __name__ == "__main__":
    main()
