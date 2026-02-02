# lifecycle/death.py

class DeathProtocol:
    """
    Graceful and final shutdown.
    """

    def __init__(self, pulse):
        self.pulse = pulse

    def execute(self):
        self.pulse.set_state("dead")
