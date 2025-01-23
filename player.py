from typing import Dict

class Player:
    """
    Represents a player in the space exploration game.
    """
    def __init__(self, name: str, fuel: int = 100) -> None:
        self.name = name
        self.health = 100  # player starts with 100 health
        self.inventory = {"fuel": fuel}  # Initialize inventory with fuel
        self.position = {"x": 0, "y": 0}  # Position in the game world
        self.current_planet = None  # player starts in space
        self.visited_planets = []  # Keep track of visited planets

    def move_up(self) -> None:
        """Move player up in the game world."""
        self.position["y"] -= 1

    def move_down(self) -> None:
        """Move player down in the game world."""
        self.position["y"] += 1

    def move_left(self) -> None:
        """Move player left in the game world."""
        self.position["x"] -= 1

    def move_right(self) -> None:
        """Move player right in the game world."""
        self.position["x"] += 1

    def visit_planet(self, planet_name: str) -> None:
        """
        Visit a new planet.
        
        Args:
            planet_name: Name of the planet to visit
        """
        self.current_planet = planet_name
        if planet_name not in self.visited_planets:
            self.visited_planets.append(planet_name)

    def collect_resource(self, resource: str, amount: int) -> None:
        """
        Collect a resource from current planet.
        
        Args:
            resource: Resource type to collect
            amount: Amount to collect
        """
        if resource in self.inventory:
            self.inventory[resource] += amount
        else:
            self.inventory[resource] = amount

    def get_status(self) -> Dict:
        """
        Get the current status of the player.
        
        Returns:
            Dict containing player's current status
        """
        return {
            "name": self.name,
            "health": self.health,
            "position": self.position,
            "current_planet": self.current_planet,
            "visited_planets": self.visited_planets,
            "inventory": self.inventory
        }

    @staticmethod
    def create_player(name: str) -> 'Player':
        """
        Factory method to create a new player.
        
        Args:
            name: The name of the new player
            
        Returns:
            A new Player instance
        """
        return Player(name)

    @staticmethod
    def load_player(player_data: Dict) -> 'Player':
        """
        Factory method to load a player from a dictionary.
        
        Args:
            player_data: Dictionary containing player data
            
        Returns:
            A Player instance
        """
        player = Player(player_data["name"], player_data["inventory"].get("fuel", 100))
        player.health = player_data.get("health", 100)
        player.position = player_data.get("position", {"x": 0, "y": 0})
        player.current_planet = player_data.get("currentPlanetId", None)
        player.visited_planets = player_data.get("visited_planets", [])
        player.inventory.update(player_data.get("inventory", {}))
        if "fuel" not in player.inventory:
            player.inventory["fuel"] = 100
        return player
