import requests

def test_move_request():
    response = requests.post(
        'http://127.0.0.1:5000/move',
        json={
            "player_id": "12345",
            "destination_planet_id": "planet789"
        },
        headers={'Content-Type': 'application/json'}
    )
    print("Status Code:", response.status_code)
    print("Response:", response.json())

if __name__ == "__main__":
    test_move_request() 