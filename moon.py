import random

class Moon:
    def __init__(self, planet_x: int, planet_y: int, orbit_radius: int):
        self.orbit_radius = orbit_radius
        self.planet_x = planet_x
        self.planet_y = planet_y
        self.angle = random.uniform(0, 360)  # Random starting position
        self.speed = random.uniform(0.5, 2.0)  # Random orbit speed
        self.update_position()
    
    def update_position(self):
        """Update moon position based on orbit angle"""
        import math
        self.x = int(self.planet_x + self.orbit_radius * math.cos(math.radians(self.angle)))
        self.y = int(self.planet_y + self.orbit_radius * math.sin(math.radians(self.angle)))
    
    def move(self):
        """Move the moon in its orbit"""
        self.angle = (self.angle + self.speed) % 360
        self.update_position()