class Asteroid:
    """
    Represents an asteroid in the space exploration game.
    """
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.visible = True
        self.crashed = False  # Track if asteroid has crashed into a planet
        
    def move_down(self, distance: int, planets) -> None:
        """Move asteroid down by the specified distance, checking for planet collisions"""
        if self.crashed:
            return
            
        new_y = self.y + distance
        self.y = new_y
        
        if self.check_planet_collision(planets):
            self.crashed = True
            self.visible = False  # Become invisible immediately on crash

    def check_planet_collision(self, planets) -> bool:
        """Check if asteroid collides with any planet"""
        if self.crashed:
            return False
            
        for planet in planets:
            if planet.is_collision(self.x, self.y):
                return True
        return False
    
    def update(self, current_time: float) -> None:
        """Update asteroid state"""
        if self.crashed and current_time - 0 > 0.5:  # Remove crash animation after 0.5 seconds
            self.visible = False