"""
A7DO Minimal Runnable Life Loop (MRLL)
TEST-LOCKED CORE + MEMORY PRUNING
"""

import time
import importlib.util
from pathlib import Path

# --------------------------------------------------
# PROJECT ROOT
# --------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]

def load_module(name: str, relative_path: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# --------------------------------------------------
# CORE
# --------------------------------------------------
self_id_mod = load_module("self_id", "00_CORE_EXISTENCE/identity/self_id.py")
clock_mod = load_module("clock", "00_CORE_EXISTENCE/heartbeat/clock.py")
pulse_mod = load_module("pulse", "00_CORE_EXISTENCE/heartbeat/pulse.py")

# --------------------------------------------------
# PHYSICS
# --------------------------------------------------
physics_mod = load_module("physics_gate", "01_PHYSICS_SANITY_SANDYS_LAW/gating.py")

# --------------------------------------------------
# METABOLISM
# --------------------------------------------------
energy_mod = load_module("energy_budget", "05_METABOLISM_AND_HOMEOSTASIS/energy_budget.py")
recovery_mod = load_module("recovery", "05_METABOLISM_AND_HOMEOSTASIS/recovery.py")
overload_mod = load_module("overload", "05_METABOLISM_AND_HOMEOSTASIS/overload.py")
regulation_mod = load_module("regulation", "05_METABOLISM_AND_HOMEOSTASIS/regulation.py")

# --------------------------------------------------
# SAFETY
# --------------------------------------------------
shutdown_mod = load_module("shutdown", "11_SAFETY_AND_GOVERNANCE/shutdown_authority.py")

# --------------------------------------------------
# BODY
# --------------------------------------------------
reflex_mod = load_module("reflex", "02_NERVOUS_SYSTEM/peripheral_nervous_system/reflexes.py")
motor_mod = load_module("motor", "03_BODY_SYSTEM/motor_control/gross_motor.py")
proprio_mod = load_module("proprio", "04_SENSORY_SYSTEM/proprioception/body_orientation.py")

# --------------------------------------------------
# MEMORY + SALIENCE
# --------------------------------------------------
episodic_mod = load_module("episodic", "07_MEMORY_SYSTEM/episodic.py")
salience_mod = load_module("salience", "06_LIMBIC_AND_VALUE_SYSTEM/salience.py")

# --------------------------------------------------
# ALIASES
# --------------------------------------------------
SelfIdentity = self_id_mod.SelfIdentity
SystemClock = clock_mod.SystemClock
Pulse = pulse_mod.Pulse

PhysicsGate = physics_mod.PhysicsGate

EnergyBudget = energy_mod.EnergyBudget
RecoverySystem = recovery_mod.RecoverySystem
OverloadMonitor = overload_mod.OverloadMonitor
HomeostasisRegulator = regulation_mod.HomeostasisRegulator

ShutdownAuthority = shutdown_mod.ShutdownAuthority

ReflexArc = reflex_mod.ReflexArc
GrossMotor = motor_mod.GrossMotor
BodyOrientationSense = proprio_mod.BodyOrientationSense

EpisodicMemory = episodic_mod.EpisodicMemory
SalienceMap = salience_mod.SalienceMap


class LifeLoop:
    def __init__(self):
        # Core
        self.identity = SelfIdentity()
        self.clock = SystemClock()      # real-world elapsed time
        self.pulse = Pulse()

        # ✅ INTERNAL (A7DO) TIME
        self.internal_time = 0

        # Physics / metabolism
        self.physics = PhysicsGate()
        self.energy = EnergyBudget(capacity=10.0)
        self.recovery = RecoverySystem(self.energy)
        self.overload = OverloadMonitor()
        self.regulator = HomeostasisRegulator(self.energy, self.overload)

        # Safety
        self.shutdown = ShutdownAuthority()

        # Body
        self.reflex = ReflexArc()
        self.motor = GrossMotor()
        self.proprio = BodyOrientationSense()

        # Memory + salience
        self.memory = EpisodicMemory()
        self.salience = SalienceMap()

    # --------------------------------------------------
    # REQUIRED BY TESTS
    # --------------------------------------------------
    def record_memory(self, event: dict, salience: float, cost: float = 0.2):
        self.physics.allow(cost, self.energy.level())
        self.energy.spend(cost)

        record = self.memory.record(event)
        memory_id = f"{event['type']}_{record['time']}"
        self.salience.set(memory_id, salience)

        return record

    def memory_recent(self, n: int = 5):
        return self.memory.recent(n)

    # --------------------------------------------------
    # LIFE TICK (INTENTIONAL EXPERIENCE)
    # --------------------------------------------------
    def tick(self):
        if not self.pulse.is_alive():
            return

        try:
            # 🔒 INTENTIONAL TIME BOUNDARY
            self.internal_time += 1
            real_time = self.clock.now()

            # Base metabolism
            self.physics.allow(1.0, self.energy.level())
            self.energy.spend(1.0)

            # Withdrawal logic (test-driven)
            if self.overload.strain > 0.5:
                # Reflex
                try:
                    self.physics.allow(0.5, self.energy.level())
                    self.energy.spend(0.5)
                    self.reflex.respond({"pain": self.overload.strain})
                except Exception:
                    pass

                # Motor
                try:
                    self.physics.allow(0.7, self.energy.level())
                    self.energy.spend(0.7)
                    action = self.motor.execute("withdraw_limb")
                except Exception:
                    action = None

                # Proprioception
                try:
                    body_state = self.proprio.sense({"action": action})
                except Exception:
                    body_state = None

                # ✅ EPISODIC MEMORY WITH DUAL TIME
                self.memory.record({
                    "type": "pain_withdrawal",
                    "body_state": body_state,
                    "time_internal": self.internal_time,
                    "time_real": real_time,
                })

            # Apply load AFTER withdrawal check
            self.overload.apply_load(0.1)

            # Memory decay / pruning
            self.memory.tick()

        except Exception as e:
            self.shutdown.trigger(str(e))
            self.pulse.set_state("dead")

    def run(self):
        while self.pulse.is_alive():
            self.tick()
            time.sleep(0.1)


# --------------------------------------------------
# ENTRY POINT
# --------------------------------------------------
if __name__ == "__main__":
    LifeLoop().run()
