# causality/no_free_work.py

class NoFreeWork:
    """
    Prevents free gain without cost.
    """

    def validate(self, input_energy, output_energy):
        if output_energy > input_energy:
            raise RuntimeError("No free work allowed")
