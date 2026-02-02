# body_schema/self_map.py

class BodySchema:
    """
    Internal map of body parts and positions.
    """

    def __init__(self):
        self.map = {}

    def update(self, part: str, position):
        self.map[part] = position

    def locate(self, part: str):
        return self.map.get(part)
