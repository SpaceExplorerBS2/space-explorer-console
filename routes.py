# FILE: routes.py
import json
from flask import Blueprint, request, jsonify

bp = Blueprint('routes', __name__)

def load_planets():
    with open('planets.json', 'r') as file:
        return json.load(file)

@bp.route('/planet', methods=['GET'])
def get_planet():
    planet_id = request.args.get('planetId')
    planets = load_planets()
    for planet in planets:
        if planet['planetId'] == planet_id:
            return jsonify(planet)
    return jsonify({"error": "Planet not found"}), 404