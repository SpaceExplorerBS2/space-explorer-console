import json
import random
from typing import Dict, List, Optional

class Planet:
    def __init__(self, x: int, y: int, size: int, planet_data: Optional[Dict] = None) -> None:
        self.x = x
        self.y = y
        self.size = size
        self.planet_id = planet_data.get('planetId') if planet_data else f"planet{random.randint(1000, 9999)}"
        self.name = planet_data.get('name', 'Unknown Planet')
        self.resources = planet_data.get('resources', {})
        self.hazards = planet_data.get('hazards', [])
        
    def is_collision(self, x: int, y: int) -> bool:
        """Check if given coordinates collide with the planet."""
        distance = ((self.x - x) ** 2 + (self.y - y) ** 2) ** 0.5
        return distance <= self.size
        
    def get_symbol(self) -> str:
        """Return the symbol to represent the planet based on its size."""
        symbols = {1: 'o', 2: 'O', 3: '@'}
        return symbols.get(self.size, 'O')
        
    def to_dict(self) -> Dict:
        """Convert planet data to dictionary format."""
        return {
            'planetId': self.planet_id,
            'name': self.name,
            'resources': self.resources,
            'hazards': self.hazards,
            'position': {'x': self.x, 'y': self.y},
            'size': self.size
        }
    
    @staticmethod
    def load_planets() -> List[Dict]:
        """Load planet data from planets.json."""
        try:
            with open('planets.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []