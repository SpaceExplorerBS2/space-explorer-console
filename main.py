# FILE: main.py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/planet', methods=['GET'])
def get_planet():
    planet_id = request.args.get('planetId')
    if planet_id == 'planet123':
        response = {
            "planetId": "planet123",
            "name": "Zorax",
            "resources": {
                "iron": 50,
                "gold": 20
            },
            "hazards": ["asteroid_field"]
        }
        return jsonify(response)
    else:
        return jsonify({"error": "Planet not found"}), 404

def main():
    print("Welcome to Space Explorer Console Game!")
    app.run(debug=True)

if __name__ == "__main__":
    main()
