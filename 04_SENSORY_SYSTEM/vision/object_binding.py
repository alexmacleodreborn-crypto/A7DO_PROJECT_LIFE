# vision/object_binding.py

class ObjectBinding:
    """
    Groups sensory features into objects.
    """

    def bind(self, features):
        return {"object": features}
