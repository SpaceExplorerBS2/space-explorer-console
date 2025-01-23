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