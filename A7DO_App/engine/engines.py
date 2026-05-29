"""
A7DO Engine Functions — All 24 engines as Python functions.
Direct mapping from Excel equations EQ_DNA_01 → EQ_LEGACY_20.
Each function mutates state in-place and returns the primary output value.
"""
import math
import random
from .state import A7DOState
from .params import A7DOParams


# ── HELPERS ───────────────────────────────────────────────────────────────────

def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))

def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))

def growth_curve(week: float, k: float = 0.005, offset: float = 40,
                 lo: float = 50, hi: float = 177) -> float:
    """Logistic growth from lo to hi."""
    if week < offset:
        return lo
    return min(lo + (hi - lo) * (1 - math.exp(-k * (week - offset))), hi)


# ── LAYER 1 — DEVELOPMENTAL ───────────────────────────────────────────────────

def EQ_DNA_01(state: A7DOState, p: A7DOParams) -> float:
    """DNA Loop Engine — master controller. Fires every tick."""
    state.week = state.tick / 80.0
    activation = clamp(state.week / 1200.0)
    state.D = clamp(state.D + p.alpha * activation + p.beta * state.phase)
    state.phase = clamp(state.phase + p.gamma * activation)
    return state.D


def EQ_ANAT_02(state: A7DOState, p: A7DOParams) -> float:
    """Anatomy Growth Engine — fires every 100 ticks."""
    w = state.week
    # Height: logistic growth
    state.height = growth_curve(w, k=0.005, offset=40, lo=50, hi=177)
    # Mass: logistic growth
    state.mass = growth_curve(w, k=0.004, offset=40, lo=3.5, hi=70)
    # Organ volume
    state.G = clamp(state.G + p.delta * state.nutrients * (1 - state.G))
    state.V_organ = state.G
    return state.G


def EQ_NEUR_03(state: A7DOState, p: A7DOParams) -> float:
    """Neural Control — fires every 10 ticks."""
    neural_gain = clamp(state.week / 1200.0)
    state.N = clamp(state.N + p.theta * neural_gain + p.iota * state.S)
    state.synapse_density = clamp(state.synapse_density + p.theta * neural_gain)
    return state.N


def EQ_CIRC_04(state: A7DOState, p: A7DOParams) -> float:
    """Circulatory — fires every tick."""
    w = state.week
    # Heart rate declines from 140 (prenatal) to 70 (adult)
    if w < 40:
        state.HR = 140.0
    else:
        state.HR = max(70.0, 140.0 - (140.0 - 70.0) * ((w - 40) / 1160.0))
    # O2 rises with development
    state.O2 = clamp(0.21 + 0.73 * clamp(w / 1200.0))
    return state.HR


def EQ_DIGE_05(state: A7DOState, p: A7DOParams) -> float:
    """Digestive & Energy — fires every 50 ticks."""
    intake = p.pi_ * state.nutrients
    activity_cost = p.rho_ * (state.motor_stage / 5.0)
    state.ATP = clamp(state.ATP + intake - activity_cost + p.sigma * (1 - state.ATP))
    return state.ATP


# ── LAYER 2 — PERCEPTION → COGNITION ─────────────────────────────────────────

def EQ_SENS_06(state: A7DOState, p: A7DOParams,
               stimulus: float = 0.5) -> float:
    """Sensory Integration — fires every tick."""
    state.S = clamp(p.tau * stimulus + p.upsilon * state.attention)
    return state.S


def EQ_EMOT_07(state: A7DOState, p: A7DOParams,
               reward: float = 0.0, punishment: float = 0.0) -> float:
    """Emotion & Reinforcement — fires every 20 ticks."""
    state.H = clamp(state.H + p.phi * reward - p.chi * punishment)
    state.reward_signal = reward - punishment
    return state.H


def EQ_PRED_08(state: A7DOState, p: A7DOParams,
               actual: float = None) -> float:
    """Predictive Simulation — fires every 5 ticks."""
    if actual is None:
        actual = state.S
    predicted = state.P_pred
    error = actual - predicted
    state.pred_error = abs(error)
    # Kalman-style update
    state.P_pred = clamp(state.P_pred + p.kappa_pred * error)
    # Free energy minimisation — error decays over time
    state.pred_error = max(0.05, state.pred_error * (1 - p.psi))
    return state.pred_error


def EQ_ATTN_09(state: A7DOState, p: A7DOParams,
               stimulus_intensity: float = 0.5) -> float:
    """Attention Control — fires every tick."""
    novelty = clamp(1.0 - state.P_pred)  # novel = unpredicted
    state.attention = clamp(
        p.alpha1 * stimulus_intensity * (1 + novelty) - p.beta1 * state.H
    )
    return state.attention


def EQ_CONS_10(state: A7DOState, p: A7DOParams) -> float:
    """Consciousness Loop — fires every 100 ticks."""
    # C integrates all internal states
    state.C = clamp(
        0.05 * state.N +
        0.15 * state.H +
        0.15 * (1 - state.pred_error) +
        0.15 * state.attention +
        0.20 * state.value +
        0.15 * state.grounding +
        0.15 * state.identity_confidence
    )
    return state.C


# ── LAYER 3 — WORLD + LANGUAGE ────────────────────────────────────────────────

def EQ_WRLD_11(state: A7DOState, p: A7DOParams) -> float:
    """World & NPC — fires every 50 ticks."""
    # World state evolves with social interaction
    social_input = sum(state.npc_bonds.values()) / len(state.npc_bonds)
    state.W_world = clamp(
        state.W_world +
        p.alpha2 * 0.5 -           # resource production
        p.beta2 * 0.3 +            # consumption
        p.gamma2 * social_input    # social enrichment
    )
    # Cultural embedding grows with world exposure
    state.cultural_embedding = clamp(
        state.cultural_embedding +
        p.eta_ce * (social_input - state.cultural_embedding)
    )
    return state.W_world


def EQ_LANG_12(state: A7DOState, p: A7DOParams) -> float:
    """Language Acquisition — fires every 10 ticks."""
    w = state.week
    # Logistic vocabulary growth: V(t) = 50000/(1+exp(-0.05*(w-156)))
    if w > 0:
        state.vocab = int(50000 / (1 + math.exp(-0.05 * (w - 156))))
    # Language state
    exposure = p.lam_lang * state.S
    reinforcement = p.mu_lang * state.H
    state.L = clamp(state.L + exposure + reinforcement)
    # Grounding grows with language + sensory
    state.grounding = clamp(
        state.grounding + 0.4 * state.S + 0.3 * state.motor_stage/5 + 0.3 * state.H
    ) * clamp(state.L)
    return state.L


# ── LAYER 4 — PHASE 3 EXPERIENTIAL ───────────────────────────────────────────

def run_proprioception(state: A7DOState, p: A7DOParams) -> None:
    """Proprioception — fires every tick."""
    # Motor stage advances with week
    w = state.week
    if   w >= 400: state.motor_stage = 5
    elif w >= 260: state.motor_stage = 4
    elif w >= 160: state.motor_stage = 3
    elif w >= 80:  state.motor_stage = 2
    else:          state.motor_stage = 1
    state.proprio = clamp(state.motor_stage / 5.0)


def run_value_system(state: A7DOState, p: A7DOParams,
                     reward: float = 0.0) -> None:
    """Value System TD(λ) — fires every 5 ticks."""
    # TD update: V(s) += η·δ
    td_error = reward + p.gamma_td * state.value - state.value
    state.value = clamp(state.value + 0.01 * td_error)
    # Attachment drive from caregiver bond
    state.attachment = clamp(state.npc_bonds.get("lorraine", 0.95) *
                              math.exp(-state.pred_error))


def run_object_permanence(state: A7DOState, p: A7DOParams) -> None:
    """Object Permanence — fires every 20 ticks."""
    w = state.week
    if   w >= 52: state.object_perm = 3
    elif w >= 44: state.object_perm = 2
    elif w >= 36: state.object_perm = 1
    else:         state.object_perm = 0


def run_episodic_memory(state: A7DOState, p: A7DOParams) -> None:
    """Episodic Memory — fires every 10 ticks (encode), 800 (consolidate)."""
    # Power-law accumulation
    if state.tick > 0:
        state.ltm_events = min(int(state.tick * 0.96), 200000)


# ── LAYER 5 — PHASE 4 COGNITIVE ───────────────────────────────────────────────

def run_language_grounding(state: A7DOState, p: A7DOParams) -> None:
    """Language Grounding G(word) — fires every 10 ticks."""
    # G(word) = Σ_m w_m·f_m(percept)
    visual_w  = 0.4 * state.S
    motor_w   = 0.3 * state.proprio
    emotion_w = 0.3 * state.H
    state.grounding = clamp(visual_w + motor_w + emotion_w)


def run_theory_of_mind(state: A7DOState, p: A7DOParams) -> None:
    """Theory of Mind — fires every 200 ticks."""
    w = state.week
    if   w >= 624: state.tom_stage = 5
    elif w >= 312: state.tom_stage = 4
    elif w >= 208: state.tom_stage = 3
    elif w >= 156: state.tom_stage = 2
    else:          state.tom_stage = 1


def run_scene_graph(state: A7DOState, p: A7DOParams) -> None:
    """Scene Graph — fires every 20 ticks."""
    # Nodes accumulate with experience
    state.scene_graph_nodes = min(
        int(state.week * 0.8 + state.ltm_events * 0.01), 500
    )


# ── PHASE 5 — CULTURAL ────────────────────────────────────────────────────────

def run_cultural_layer(state: A7DOState, p: A7DOParams) -> None:
    """Cultural embedding — fires every 50 ticks."""
    norm_exposure = state.W_world * sum(state.npc_bonds.values()) / 4
    state.cultural_embedding = clamp(
        state.cultural_embedding + p.eta_ce * (norm_exposure - state.cultural_embedding)
    )


# ── PHASE 6 — IDENTITY ────────────────────────────────────────────────────────

def run_identity_layer(state: A7DOState, p: A7DOParams) -> None:
    """Identity formation — fires every 100 ticks."""
    # Narrative coherence from episodic memory + self-model
    if state.ltm_events > 0:
        state.narrative_coherence = clamp(
            state.C * 0.4 + state.grounding * 0.3 + state.cultural_embedding * 0.3
        )
    # Identity confidence from stability
    state.identity_confidence = clamp(
        state.narrative_coherence * state.value * (state.week / 1200.0)
    )
    # Skill vector grows with practice
    for i in range(22):
        state.skill_vector[i] = clamp(
            state.skill_vector[i] + p.eta_s * state.L * 0.01
        )


# ── PHASE 7 — WISDOM ──────────────────────────────────────────────────────────

def EQ_CREAT_17(state: A7DOState, p: A7DOParams) -> float:
    """Creative Synthesis — fires every 500 ticks (Phase 7 only)."""
    if state.tick < 96000:
        return 0.0
    # C_new(t) = α_c·(M_episodic ⊕ M_semantic) + β_c·(P_sim ⊗ S_skills) + γ_c·Noise
    memory_blend = p.alpha_c * (state.ltm_events / 200000.0 + state.grounding) / 2
    skill_pred   = p.beta_c  * (1 - state.pred_error) * (sum(state.skill_vector) / 22)
    noise        = p.gamma_c * random.gauss(0, 0.1)
    state.creativity = clamp(memory_blend + skill_pred + noise)
    return state.creativity


def EQ_WISDOM_18(state: A7DOState, p: A7DOParams) -> float:
    """Wisdom Index — fires every 500 ticks (Phase 7 only)."""
    if state.tick < 96000:
        state.wisdom = 0.0
        return 0.0
    # W(t+1) = W(t) + η_w·[λ1·C50yr + λ2·EthicalWeight + λ3·EmpathyIndex − λ4·ImpulseDrive]
    consequence_50yr = clamp((state.week - 1200) / 800.0)
    ethical_weight   = state.cultural_embedding
    empathy_index    = sum(state.npc_bonds.values()) / len(state.npc_bonds) * state.tom_stage / 5
    impulse_drive    = clamp(1 - state.attention + (1 - state.value))
    delta_w = p.eta_w * (
        p.lam1 * consequence_50yr +
        p.lam2 * ethical_weight +
        p.lam3 * empathy_index -
        p.lam4 * impulse_drive
    )
    state.wisdom = clamp(state.wisdom + delta_w)
    return state.wisdom


def EQ_CAREER_19(state: A7DOState, p: A7DOParams) -> float:
    """Career Specialisation — fires every 1000 ticks (Phase 7 only)."""
    if state.tick < 96000:
        return 0.0
    skill_avg = sum(state.skill_vector) / 22
    opportunity = state.W_world
    identity_v  = state.identity_confidence
    state.career = clamp(
        state.career + p.eta_car * skill_avg * opportunity * identity_v
    )
    return state.career


def EQ_LEGACY_20(state: A7DOState, p: A7DOParams) -> float:
    """Legacy Projection — fires every 2000 ticks (Phase 7 only)."""
    if state.tick < 96000:
        return 0.0
    impact_direct   = state.value * state.wisdom
    impact_indirect = state.cultural_embedding * sum(state.npc_bonds.values()) / 4
    cultural_trans  = state.creativity * state.grounding
    entropy         = p.entropy_f * state.legacy
    state.legacy = max(0.0,
        state.legacy + p.eta_l * (impact_direct + impact_indirect + cultural_trans - entropy)
    )
    return state.legacy


# ── LEARNING LOOP ─────────────────────────────────────────────────────────────

def run_learning_loop_phase(state: A7DOState, p: A7DOParams,
                             stimulus: float = 0.5,
                             reward: float = 0.0) -> str:
    """Determine and execute current learning loop phase."""
    tick = state.tick
    if tick % 800 == 0:
        # Stage 4 — Sleep Consolidation
        state.ll_phase = "Sleep Consolidation"
        # Episodic → semantic transfer
        state.grounding = clamp(state.grounding + 0.01 * state.ltm_events / 10000)
        state.pred_error = max(0.05, state.pred_error * 0.9)
        run_episodic_memory(state, p)
    elif tick % 10 == 0:
        # Stage 3 — Repetition
        state.ll_phase = "Repetition"
        run_language_grounding(state, p)
        run_theory_of_mind(state, p)
        run_scene_graph(state, p)
    elif tick % 5 == 0:
        # Stage 2 — Interaction
        state.ll_phase = "Interaction"
        EQ_PRED_08(state, p, actual=stimulus)
        run_value_system(state, p, reward=reward)
        run_object_permanence(state, p)
    else:
        # Stage 1 — Exposure
        state.ll_phase = "Exposure"
        EQ_SENS_06(state, p, stimulus=stimulus)
        EQ_ATTN_09(state, p, stimulus_intensity=stimulus)
        EQ_EMOT_07(state, p, reward=reward * 0.5)
    return state.ll_phase