"""
A7DO Life Loop
Physics-governed, sleep-aware, memory-producing organism loop
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
sleep_mod = load_module("sleep", "00_CORE_EXISTENCE/heartbeat/sleep_wake.py")

# --------------------------------------------------
# WORLD
# --------------------------------------------------
world_time_mod = load_module("world_time", "09_WORLD_MODEL/time.py")
world_state_mod = load_module("world_state", "09_WORLD_MODEL/world_state.py")

# --------------------------------------------------
# PHYSICS — ENERGY
# --------------------------------------------------
unified_energy_mod = load_module(
    "unified_energy",
    "01_PHYSICS_SANITY_SANDYS_LAW/energy/unified_energy.py"
)
metabolism_mod = load_module(
    "metabolism",
    "01_PHYSICS_SANITY_SANDYS_LAW/energy/metabolism.py"
)
fatigue_mod = load_module(
    "fatigue",
    "01_PHYSICS_SANITY_SANDYS_LAW/energy/fatigue.py"
)

# --------------------------------------------------
# BODY
# --------------------------------------------------
motor_mod = load_module("motor", "03_BODY_SYSTEM/motor_control/gross_motor.py")
proprio_mod = load_module("proprio", "04_SENSORY_SYSTEM/proprioception/body_orientation.py")

# --------------------------------------------------
# MEMORY
# --------------------------------------------------
episodic_mod = load_module("episodic", "07_MEMORY_SYSTEM/episodic.py")

# --------------------------------------------------
# ALIASES
# --------------------------------------------------
SelfIdentity = self_id_mod.SelfIdentity
SystemClock = clock_mod.SystemClock
Pulse = pulse_mod.Pulse
SleepWakeCycle = sleep_mod.SleepWakeCycle

WorldTime = world_time_mod.WorldTime
WorldState = world_state_mod.WorldState

UnifiedEnergy = unified_energy_mod.UnifiedEnergy
Metabolism = metabolism_mod.Metabolism
Fatigue = fatigue_mod.Fatigue

GrossMotor = motor_mod.GrossMotor
BodyOrientationSense = proprio_mod.BodyOrientationSense

EpisodicMemory = episodic_mod.EpisodicMemory


class LifeLoop:
    """
    The only place A7DO experiences time.
    LifeLoop orchestrates — physics decides.
    """

    def __init__(self):
        # Core
        self.identity = SelfIdentity()
        self.clock = SystemClock()
        self.pulse = Pulse()
        self.sleep_wake = SleepWakeCycle()

        # Time
        self.internal_time = 0
        self.world_time = WorldTime()
        self.world = WorldState()

        # Physics
        self.energy = UnifiedEnergy(capacity=10.0)
        self.metabolism = Metabolism(self.energy)
        self.fatigue = Fatigue()

        # Body
        self.motor = GrossMotor()
        self.proprio = BodyOrientationSense()

        # Memory
        self.memory = EpisodicMemory()

    # --------------------------------------------------
    # LIFE TICK
    # --------------------------------------------------
    def tick(self):
        if not self.pulse.is_alive():
            return

        try:
            # ------------------------------------------
            # TIME
            # ------------------------------------------
            self.internal_time += 1
            real_time = self.clock.now()
            self.world_time.tick(delta=1.0)

            # ------------------------------------------
            # SLEEP / WAKE DECISION (WITH HYSTERESIS)
            # ------------------------------------------
            if self.fatigue.level >= 0.7:
                self.sleep_wake.sleep()
            elif self.fatigue.level <= 0.3:
                self.sleep_wake.wake()

            awake = self.sleep_wake.awake

            # ------------------------------------------
            # PHYSICS ENERGY UPDATE (ONCE)
            # ------------------------------------------
            self.energy.tick(
                awake=awake,
                strain=self.fatigue.level,
                delta_t=1.0,
                activity_cost=0.0
            )

            # ------------------------------------------
            # BASELINE FATIGUE / RECOVERY
            # ------------------------------------------
            if awake:
                self.fatigue.add(0.05)
            else:
                self.fatigue.recover(0.1)

            # ------------------------------------------
            # ACTION PHASE
            # ------------------------------------------
            action = None
            body_state = None

            if awake and self.fatigue.level > 0.5:
                # Motor action
                self.metabolism.spend(0.6)
                action = self.motor.execute("withdraw_limb")

                # Extra fatigue from action
                self.fatigue.add(0.2)

                body_state = self.proprio.sense({"action": action})

                # Record episodic memory (REQUIRED)
                self.memory.record({
                    "type": "pain_withdrawal",
                    "action": action,
                    "body_state": body_state,
                    "time_internal": self.internal_time,
                    "time_real": real_time,
                    "time_world": self.world_time.t,
                })

            # ------------------------------------------
            # WORLD SNAPSHOT (FOR DASHBOARD)
            # ------------------------------------------
            self.world.update(
                energy=self.energy.level,
                strain=self.fatigue.level,
                last_action=action,
                time=self.world_time.t,
            )

            # ------------------------------------------
            # MEMORY MAINTENANCE
            # ------------------------------------------
            self.memory.tick()

            # ------------------------------------------
            # TERMINATION
            # ------------------------------------------
            if self.energy.is_depleted():
                self.pulse.set_state("dead")

        except Exception:
            self.pulse.set_state("dead")

    # --------------------------------------------------
    # HELPERS FOR DASHBOARD / TESTS
    # --------------------------------------------------
    def recent_memory(self, n=5):
        return self.memory.recent(n)

    def snapshot(self):
        return {
            "world": self.world.snapshot(),
            "energy": self.energy.snapshot(),
            "fatigue": self.fatigue.level,
            "awake": self.sleep_wake.awake,
            "alive": self.pulse.is_alive(),
        }

    def run(self, delay: float = 0.1):
        while self.pulse.is_alive():
            self.tick()
            time.sleep(delay)


# --------------------------------------------------
# ENTRY POINT
# --------------------------------------------------
if __name__ == "__main__":
    LifeLoop().run()
