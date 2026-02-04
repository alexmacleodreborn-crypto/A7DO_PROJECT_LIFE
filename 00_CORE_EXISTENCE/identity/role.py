class Role:
    """
    Defines A7DO's functional role in the current interaction.
    """

    def __init__(self, role_name="observer"):
        self.role_name = role_name

    def get_role(self):
        return self.role_name

    def set_role(self, role_name):
        self.role_name = role_name
