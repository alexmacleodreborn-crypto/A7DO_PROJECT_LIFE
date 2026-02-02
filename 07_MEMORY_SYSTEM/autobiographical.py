# autobiographical.py

class AutobiographicalMemory:
    """
    Maintains the narrative of self over time.
    """

    def __init__(self):
        self.timeline = []

    def append(self, summary: str):
        self.timeline.append(summary)

    def story(self):
        return list(self.timeline)
