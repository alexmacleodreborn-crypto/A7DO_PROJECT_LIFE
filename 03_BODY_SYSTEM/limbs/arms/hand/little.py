# limbs/arms/hand/little.py

class Little:
    """
    Independent digit control.
    """

    def __init__(self):
        self.flexed = False

    def flex(self):
        self.flexed = True

    def extend(self):
        self.flexed = False
