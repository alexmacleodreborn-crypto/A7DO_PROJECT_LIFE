from identity.naming import NamingSystem
from identity.persona import Persona
from identity.role import Role

class IdentityCore:
    """
    Central identity container for A7DO.
    """

    def __init__(self):
        self.naming = NamingSystem()
        self.persona = Persona()
        self.role = Role()

    def snapshot(self):
        return {
            "name": self.naming.get_self_name(),
            "persona": self.persona.describe(),
            "role": self.role.get_role()
        }
