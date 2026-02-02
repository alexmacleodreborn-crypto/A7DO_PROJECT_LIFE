# lifecycle/transitions.py

from .stages import LifeStage

VALID_TRANSITIONS = {
    LifeStage.SEED: LifeStage.WOMB,
    LifeStage.WOMB: LifeStage.BIRTH,
    LifeStage.BIRTH: LifeStage.INFANT,
    LifeStage.INFANT: LifeStage.CHILD,
    LifeStage.CHILD: LifeStage.ADOLESCENT,
    LifeStage.ADOLESCENT: LifeStage.ADULT,
}

class LifecycleManager:
    def __init__(self):
        self.stage = LifeStage.SEED

    def advance(self):
        if self.stage not in VALID_TRANSITIONS:
            raise RuntimeError("Invalid lifecycle transition")
        self.stage = VALID_TRANSITIONS[self.stage]
        return self.stage
