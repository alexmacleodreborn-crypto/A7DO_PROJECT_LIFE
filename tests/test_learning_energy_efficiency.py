import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load_modules():
    learn_path = ROOT / "03_BODY_SYSTEM/motor_control/energy_learning.py"
    mem_path = ROOT / "07_MEMORY_SYSTEM/episodic.py"
    att_path = ROOT / "06_LIMBIC_AND_VALUE_SYSTEM/attention.py"

    # Load learner
    learn_spec = importlib.util.spec_from_file_location("energy_learning", learn_path)
    learn_mod = importlib.util.module_from_spec(learn_spec)
    learn_spec.loader.exec_module(learn_mod)

    # Load memory
    mem_spec = importlib.util.spec_from_file_location("episodic", mem_path)
    mem_mod = importlib.util.module_from_spec(mem_spec)
    mem_spec.loader.exec_module(mem_mod)

    # Load attention
    att_spec = importlib.util.spec_from_file_location("attention", att_path)
    att_mod = importlib.util.module_from_spec(att_spec)
    att_spec.loader.exec_module(att_mod)

    return learn_mod.ActionEnergyLearner, mem_mod.EpisodicMemory, att_mod.AttentionSystem


def test_repeated_action_cost_decreases():
    Learner, Memory, Attention = load_modules()

    mem = Memory(capacity=10)
    att = Attention(mem, focus_size=3)
    learner = Learner(decay=0.05, floor=0.3)

    # Repeated, highly salient action
    for _ in range(5):
        mem.record(
            {"type": "action", "name": "withdraw_limb"},
            salience=0.9
        )
        learner.learn(att.focus())

    base_cost = 1.0
    learned_cost = learner.cost("withdraw_limb", base_cost)

    assert learned_cost < base_cost, "Repeated action should become cheaper"
    assert learned_cost >= 0.3, "Cost must not fall below floor"


def test_unattended_actions_do_not_learn():
    Learner, Memory, Attention = load_modules()

    mem = Memory(capacity=10)
    att = Attention(mem, focus_size=1)
    learner = Learner(decay=0.05, floor=0.3)

    # Low-salience action (never attended)
    for _ in range(5):
        mem.record(
            {"type": "action", "name": "rare_action"},
            salience=0.01
        )
        learner.learn(att.focus())

    base_cost = 1.0
    learned_cost = learner.cost("rare_action", base_cost)

    assert learned_cost == base_cost, "Unattended actions must not learn"

