# limbs/arms/hand/palm.py

class Palm:
    """
    Central structure connecting fingers.
    """

    def __init__(self):
        self.open = True

    def open_hand(self):
        self.open = True

    def close_hand(self):
        self.open = False
