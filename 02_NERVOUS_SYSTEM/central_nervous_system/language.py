# central_nervous_system/language.py

class LanguageInterface:
    """
    Handles symbolic language processing.
    """

    def encode(self, text: str) -> dict:
        return {"tokens": text.split()}

    def decode(self, representation: dict) -> str:
        return " ".join(representation.get("tokens", []))
