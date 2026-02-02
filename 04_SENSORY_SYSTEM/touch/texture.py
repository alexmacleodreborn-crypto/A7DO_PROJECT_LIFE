# touch/texture.py

class TextureSensor:
    """
    Surface roughness detection.
    """

    def read(self, surface):
        return {"texture": surface}
