# olfaction/memory_link.py

class SmellMemoryLink:
    """
    Associates smells with memory keys.
    """

    def associate(self, smell, memory_id):
        return {"smell": smell, "memory": memory_id}
