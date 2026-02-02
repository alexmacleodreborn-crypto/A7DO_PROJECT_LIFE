# coupling/photon.py

class PhotonCoupling:
    """
    Information transmission cost.
    """

    def transmit(self, info: float, noise: float = 0.01) -> float:
        return max(0.0, info - noise)
