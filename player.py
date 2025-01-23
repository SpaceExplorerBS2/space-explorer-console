from typing import Dict

class Player:
    """
    Represents a player in the space exploration game.
    """
    def __init__(self, name: str) -> None:
        self.name = name
        self.health = 100  # player starts with 100 health
        self.fuel = 100    # player starts with 100 fuel
        self.inventory = {}  # by default empty inventory
        self.position = {"x": 0, "y": 0}  # Position in the game world
        self.current_planet = None  # player starts in space
        self.visited_planets = []  # Keep track of visited planets

    def move_up(self) -> None:
        """Move player up in the game world."""
        if self.use_fuel():
            self.position["y"] -= 1

    def move_down(self) -> None:
        """Move player down in the game world."""
        if self.use_fuel():
            self.position["y"] += 1

    def move_left(self) -> None:
        """Move player left in the game world."""
        if self.use_fuel():
            self.position["x"] -= 1

    def move_right(self) -> None:
        """Move player right in the game world."""
        if self.use_fuel():
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

    def use_fuel(self, amount: int = 1) -> bool:
        """
        Use fuel for movement.
        
        Args:
            amount: Amount of fuel to use
            
        Returns:
            bool: True if enough fuel was available, False otherwise
        """
        if self.fuel >= amount:
            self.fuel -= amount
            return True
        return False

    def add_fuel(self, amount: int) -> None:
        """
        Add fuel to the player.
        
        Args:
            amount: Amount of fuel to add
        """
        self.fuel = min(100, self.fuel + amount)  # Cap at 100

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
            "inventory": self.inventory,
            "fuel": self.fuel
        }

    @classmethod
    def from_dict(cls, player_data: dict) -> 'Player':
        """
        Create a Player instance from a dictionary.
        
        Args:
            player_data: Dictionary containing player data
            
        Returns:
            A Player instance
        """
        player = Player(player_data["name"])
        player.health = player_data.get("health", 100)
        player.fuel = player_data.get("fuel", 100)
        player.position = player_data.get("position", {"x": 0, "y": 0})
        player.current_planet = player_data.get("currentPlanetId", None)
        player.visited_planets = player_data.get("visited_planets", [])
        player.inventory = player_data.get("inventory", {})
        return player