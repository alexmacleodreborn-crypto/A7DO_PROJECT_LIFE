# environments/home.py

class HomeEnvironment:
    """
    Controlled, predictable environment.
    """

    def __init__(self):
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)
