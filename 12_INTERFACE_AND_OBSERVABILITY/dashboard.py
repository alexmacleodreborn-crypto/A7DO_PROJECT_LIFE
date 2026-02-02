# dashboard.py

class Dashboard:
    """
    Aggregates system state for display.
    """

    def __init__(self):
        self.panels = {}

    def update_panel(self, name: str, data: dict):
        self.panels[name] = data

    def render(self) -> dict:
        return self.panels
