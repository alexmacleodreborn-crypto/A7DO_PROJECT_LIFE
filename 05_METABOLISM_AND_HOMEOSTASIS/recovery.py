"""
RecoverySystem — metabolic restoration

Loaded via importlib by file path.
All dependencies must also be loaded explicitly.
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
# Load EnergyBudget explicitly
# --------------------------------------------------
energy_mod = load_local_module(
    "energy_budget",
    "energy_budget.py"
)

EnergyBudget = energy_mod.EnergyBudget


class RecoverySystem:
    """
    Handles energy restoration during rest.
    """

    def __init__(self, energy_budget: EnergyBudget):
        self.energy = energy_budget

    def rest(self, duration: float):
        restore = duration * 0.1
        self.energy.replenish(restore)
