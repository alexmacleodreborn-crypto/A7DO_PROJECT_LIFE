# limbs/legs/foot.py

class Foot:
    """
    Contact with environment.
    """

    def __init__(self):
        self.contact = False

    def touch_ground(self):
        self.contact = True

    def lift(self):
        self.contact = False
