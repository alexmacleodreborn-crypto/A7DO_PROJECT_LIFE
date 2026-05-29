"""
A7DO Runtime — Canonical Tick Loop
Replaces the surrogate organism_state() function.
Executes all 24 engines in correct layer order.
"""
import random
from .state import A7DOState
from .params import A7DOParams
from .engines import (
    EQ_DNA_01, EQ_ANAT_02, EQ_NEUR_03, EQ_CIRC_04, EQ_DIGE_05,
    EQ_SENS_06, EQ_EMOT_07, EQ_PRED_08, EQ_ATTN_09, EQ_CONS_10,
    EQ_WRLD_11, EQ_LANG_12,
    run_proprioception, run_value_system, run_object_permanence,
    run_episodic_memory, run_language_grounding, run_theory_of_mind,
    run_scene_graph, run_cultural_layer, run_identity_layer,
    EQ_CREAT_17, EQ_WISDOM_18, EQ_CAREER_19, EQ_LEGACY_20,
    run_learning_loop_phase,
)


def step(state: A7DOState, params: A7DOParams,
         stimulus: float = None, reward: float = None) -> A7DOState:
    """
    Execute one tick of the A7DO organism.
    Fires all 24 engines in correct layer order.
    """
    tick = state.tick

    # Generate environmental stimulus if not provided
    if stimulus is None:
        stimulus = 0.3 + 0.4 * random.random()
    if reward is None:
        reward = 0.05 * random.random()

    # ── LAYER 1 — Developmental (every tick) ──────────────────────────────────
    EQ_DNA_01(state, params)
    EQ_CIRC_04(state, params)
    EQ_SENS_06(state, params, stimulus=stimulus)
    EQ_ATTN_09(state, params, stimulus_intensity=stimulus)
    run_proprioception(state, params)

    # ── LAYER 1 — Slower developmental ────────────────────────────────────────
    if tick % 10 == 0:
        EQ_NEUR_03(state, params)
    if tick % 50 == 0:
        EQ_DIGE_05(state, params)
    if tick % 100 == 0:
        EQ_ANAT_02(state, params)

    # ── LAYER 2 — Perception → Cognition ──────────────────────────────────────
    if tick % 5 == 0:
        EQ_PRED_08(state, params, actual=stimulus)
    if tick % 20 == 0:
        EQ_EMOT_07(state, params, reward=reward, punishment=0.0)
    if tick % 100 == 0:
        EQ_CONS_10(state, params)

    # ── LAYER 3 — World + Language ────────────────────────────────────────────
    if tick % 10 == 0:
        EQ_LANG_12(state, params)
    if tick % 50 == 0:
        EQ_WRLD_11(state, params)

    # ── LAYER 4 — Phase 3 Experiential ────────────────────────────────────────
    if tick % 5 == 0:
        run_value_system(state, params, reward=reward)
    if tick % 10 == 0:
        run_episodic_memory(state, params)
    if tick % 20 == 0:
        run_object_permanence(state, params)

    # ── LAYER 5 — Phase 4 Cognitive ───────────────────────────────────────────
    if tick % 10 == 0:
        run_language_grounding(state, params)
    if tick % 20 == 0:
        run_scene_graph(state, params)
    if tick % 200 == 0:
        run_theory_of_mind(state, params)

    # ── LAYER 5 — Phase 5 & 6 ────────────────────────────────────────────────
    if tick % 50 == 0:
        run_cultural_layer(state, params)
    if tick % 100 == 0:
        run_identity_layer(state, params)

    # ── LAYER 6 — Phase 7 Wisdom (tick >= 96000) ──────────────────────────────
    if tick % 500 == 0:
        EQ_CREAT_17(state, params)
        EQ_WISDOM_18(state, params)
    if tick % 1000 == 0:
        EQ_CAREER_19(state, params)
    if tick % 2000 == 0:
        EQ_LEGACY_20(state, params)

    # ── Learning Loop ─────────────────────────────────────────────────────────
    run_learning_loop_phase(state, params, stimulus=stimulus, reward=reward)

    # ── Advance tick ──────────────────────────────────────────────────────────
    state.tick += 1

    # ── Record history (keep last 200 snapshots) ──────────────────────────────
    if tick % 80 == 0:  # record every week
        state.history.append(state.snapshot())
        if len(state.history) > 200:
            state.history.pop(0)

    return state


def jump_to_tick(target_tick: int, params: A7DOParams = None,
                 record_every: int = 80) -> A7DOState:
    """
    Fast-forward organism to target_tick.
    Returns state at target_tick with history recorded every record_every ticks.
    """
    if params is None:
        params = A7DOParams()
    state = A7DOState()
    # Seed initial conditions
    state.nutrients = 1.0
    state.npc_bonds = {"lorraine": 0.95, "alexis": 0.70, "evelyn": 0.65, "james": 0.30}

    random.seed(42)  # deterministic fast-forward
    for t in range(target_tick):
        # Vary stimulus slightly for realism
        stimulus = 0.3 + 0.4 * math.sin(t / 100.0 + 0.5) * 0.5 + 0.2
        reward   = 0.05 + 0.03 * (t % 800 == 0)  # extra reward on sleep
        step(state, params, stimulus=stimulus, reward=reward)

    return state


def run_sim(state: A7DOState, params: A7DOParams,
            ticks: int = 1000, record_every: int = 80,
            verbose: bool = False):
    """
    Run simulation for N ticks from current state.
    Returns list of snapshots.
    """
    snapshots = []
    for t in range(ticks):
        stimulus = 0.3 + 0.4 * random.random()
        reward   = 0.05 * random.random()
        step(state, params, stimulus=stimulus, reward=reward)
        if t % record_every == 0:
            snap = state.snapshot()
            snapshots.append(snap)
            if verbose:
                print(f"Tick {state.tick}: Week {snap['week']:.1f} | "
                      f"Stage {state.life_stage()} | "
                      f"C={snap['C']:.3f} | Vocab={snap['vocab']:,}")
    return snapshots


# Fix missing import
import math