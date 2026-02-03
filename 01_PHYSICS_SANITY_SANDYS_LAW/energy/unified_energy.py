# energy/unified_energy.py

class UnifiedEnergy:
    """
    Physics-level energy law.

    Computes energy flow per tick based on:
    - basal metabolism
    - activity cost
    - sleep / rest recovery
    - fatigue / strain penalty
    """

    def __init__(
        self,
        capacity: float = 10.0,
        basal_cost: float = 0.2,
        recovery_rate: float = 0.4,
        fatigue_penalty: float = 0.5,
    ):
        self.capacity = capacity
        self.level = capacity

        self.basal_cost = basal_cost
        self.recovery_rate = recovery_rate
        self.fatigue_penalty = fatigue_penalty

    # --------------------------------------------------
    # CORE PHYSICS
    # --------------------------------------------------
    def tick(
        self,
        *,
        awake: bool,
        strain: float,
        delta_t: float = 1.0,
        activity_cost: float = 0.0,
    ):
        """
        Advance energy state by one tick.

        Parameters
        ----------
        awake : bool
            Whether system is awake or sleeping.
        strain : float
            Current fatigue / overload level (0..1).
        delta_t : float
            Time step (world or internal time).
        activity_cost : float
            Cost of intentional actions this tick.
        """

        # --- Basal metabolism always applies ---
        energy_change = -self.basal_cost * delta_t

        # --- Activity cost ---
        energy_change -= activity_cost

        # --- Fatigue penalty (only when awake) ---
        if awake:
            energy_change -= self.fatigue_penalty * strain * delta_t

        # --- Recovery (only when sleeping) ---
        if not awake:
            energy_change += self.recovery_rate * delta_t

        # Apply change
        self.level += energy_change

        # Clamp to bounds
        if self.level > self.capacity:
            self.level = self.capacity

        if self.level < 0:
            self.level = 0

        return self.level

    # --------------------------------------------------
    # HARD CONSTRAINT
    # --------------------------------------------------
    def consume(self, amount: float):
        """
        Immediate energy consumption (forced action).
        """
        if amount > self.level:
            raise RuntimeError("Energy budget exceeded")
        self.level -= amount

    # --------------------------------------------------
    # STATE
    # --------------------------------------------------
    def is_depleted(self) -> bool:
        return self.level <= 0

    def snapshot(self) -> dict:
        return {
            "energy": self.level,
            "capacity": self.capacity,
        }
