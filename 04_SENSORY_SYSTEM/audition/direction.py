# audition/direction.py

class SoundDirection:
    """
    Estimates sound origin.
    """

    def locate(self, waveform):
        return {"direction": "unknown"}
