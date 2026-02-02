# limbs/arms/hand/Middle.py

class Middle:
    """
    Independent digit control.
    """

    def __init__(self):
        self.flexed = False

    def flex(self):
        self.flexed = True

    def extend(self):
        self.flexed = False
