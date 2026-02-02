"""
PhysicsGate — Sandy’s Law choke point

This file is loaded via importlib by path.
Therefore ALL dependencies must also be loaded by path.
"""

import importlib.util
from pathlib import Path

# --------------------------------------------------
# Resolve folder path
# --------------------------------------------------
HERE = Path(__file__).resolve().parent

def load_local_module(name: str, filename: str):
    path = HERE / filename
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# --------------------------------------------------
# Load ConservationLaw explicitly
# --------------------------------------------------
conservation_mod = load_local_module(
    "conservation",
    "conservation.py"
)

ConservationLaw = conservation_mod.ConservationLaw


class PhysicsGate:
    """
    All signals must pass through Sandy’s Law gating.
    """

    def __init__(self):
        self.conservation = ConservationLaw()

    def allow(self, energy_cost: float, available_energy: float) -> bool:
        self.conservation.check(energy_cost, available_energy)
        return True
