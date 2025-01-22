import Flask

class Player:
    def __init__(player, name: str):
        player.name = name
        player.inventory = {"iron": 0, "gold": 0}
        player.current_planet = None
        player.ID = None
        


