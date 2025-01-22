import Flask

class Player:
    def __init__(self, name: str):
        self.name = name
        self.resources = {"iron": 0, "gold": 0}
