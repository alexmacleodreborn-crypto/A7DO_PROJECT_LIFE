# central_nervous_system/attention.py

class Attention:
    """
    Selects which signals reach higher processing.
    """

    def __init__(self):
        self.focus = None

    def set_focus(self, signal_id):
        self.focus = signal_id

    def get_focus(self):
        return self.focus
