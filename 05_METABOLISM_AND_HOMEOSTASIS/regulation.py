"""
HomeostasisRegulator — internal stability control

Loaded via importlib by file path.
All dependencies must be loaded explicitly.
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
# Load dependencies explicitly
# --------------------------------------------------
energy_mod = load_local_module(
    "energy_budget",
    "energy_budget.py"
)
overload_mod = load_local_module(
    "overload",
    "overload.py"
)

EnergyBudget = energy_mod.EnergyBudget
OverloadMonitor = overload_mod.OverloadMonitor


class HomeostasisRegulator:
    """
    Maintains internal stability.
    """

    def __init__(self, energy_budget: EnergyBudget, overload: OverloadMonitor):
        self.energy = energy_budget
        self.overload = overload

    def regulate(self):
        if self.energy.level() < 0.2 * self.energy.capacity:
            return "rest"
        if self.overload.strain > 0.7:
            return "reduce_activity"
        return "stable"
