class Player:

    def __init__(self, id, x, y, health):
        super().__init__()
        self.id = id
        self.x = x
        self.y = y
        self.health = health

    def get_player_data(self):
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "health": self.health,
            # Add any other relevant data you want to send
        }

    def update_from_data(self, data):
        if data is not None:
            self.id = data["id"]
            self.x = data["x"]
            self.y = data["y"]
            self.health = data["health"]
            # Update any other relevant data you received
