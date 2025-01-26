class Asteroid:
    """
    Represents an asteroid in the space exploration game.
    """
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.visible = True
        
    def move_down(self, distance: int) -> None:
        """Move asteroid down by the specified distance."""
        self.y += distance


    def check_planet_collision(self, planets) -> bool:
        """Check if asteroid collides with any planet"""
        for planet in planets:
            if planet.is_collision(self.x, self.y):
                return True
        return False
    
    def move_down(self, distance: int, planets) -> None:
        """Move asteroid down by the specified distance, checking for planet collisions"""
        new_y = self.y + distance
        # Create temporary position to check collision
        old_y = self.y
        self.y = new_y
        if self.check_planet_collision(planets):
            self.y = old_y  # Revert position if collision detected