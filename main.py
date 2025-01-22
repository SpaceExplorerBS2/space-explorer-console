# FILE: main.py
import json
from flask import Flask, request, jsonify
from routes import bp as routes_bp

app = Flask(__name__)
app.register_blueprint(routes_bp)

def load_planets():
    with open('planets.json', 'r') as file:
        return json.load(file)

@app.route('/planet', methods=['GET'])
def get_planet():
    planet_id = request.args.get('planetId')
    planets = load_planets()
    for planet in planets:
        if planet['planetId'] == planet_id:
            return jsonify(planet)
    return jsonify({"error": "Planet not found"}), 404

def main():
    print("Welcome to Space Explorer Console Game!")
    app.run(debug=True)

if __name__ == "__main__":
    main()
