# vision/retina.py

class Retina:
    """
    Raw visual input grid.
    """

    def capture(self, frame):
        # frame = raw pixel/light data
        return {"raw_frame": frame}
