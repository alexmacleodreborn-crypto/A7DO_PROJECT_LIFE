# environments/weather_system.py

class WeatherSystem:
    """
    Weather evolves independently.
    """

    def __init__(self):
        self.state = "clear"

    def update(self, new_state: str):
        self.state = new_state
