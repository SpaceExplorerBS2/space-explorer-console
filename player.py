from typing import Dict

class Player:
    """
    Represents a player in the space exploration game.
    """
    def __init__(self, name: str) -> None:
        self.name = name
        self.health = 100 # player starts with 100 health
        self.inventory = {} #by default empty inventory
        self.position = {"x": 0, "y": 0}  # Position in the game world
        self.current_planet = None # player starts in space
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
            self.inventory.append[resource] = amount 
        
        print(f"Du hast {amount} Einheiten {resource} gesammelt.")
        """
        Resources have been collected.
        """
        print("In deinem Inventar befindet sich gerade:")
        for x in self.inventory:
            print(self.inventory[x])

        print("\n Alle Ressourcen von diesem Planeten wurden bereits gesammelt.")

        """
        This planet has no more resources left to gather
        """

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
