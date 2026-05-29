"""
A7DO State Object — Central Organism Memory
All state variables for the 24-engine runtime.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any
import math


@dataclass
class A7DOState:
    # ── Core tick ──────────────────────────────────────────────────────────────
    tick: int = 0
    week: float = 0.0

    # ── Phase 1 — Biology ─────────────────────────────────────────────────────
    D: float = 0.0          # EQ_DNA_01 — DNA loop state
    phase: float = 0.0      # Developmental phase index
    G: float = 0.0          # EQ_ANAT_02 — Anatomy growth
    V_organ: float = 0.0    # Organ volume
    height: float = 50.0    # cm
    mass: float = 3.5       # kg
    N: float = 0.0          # EQ_NEUR_03 — Neural state
    synapse_density: float = 0.0
    HR: float = 140.0       # EQ_CIRC_04 — Heart rate bpm
    O2: float = 0.21        # Blood oxygen
    ATP: float = 0.5        # EQ_DIGE_05 — Energy
    nutrients: float = 1.0

    # ── Phase 2 — Sensorimotor ────────────────────────────────────────────────
    S: float = 0.0          # EQ_SENS_06 — Sensory integration
    attention: float = 0.0  # EQ_ATTN_09 — Attention
    reflex_gain: float = 0.0
    motor_stage: int = 1    # 1-5
    proprio: float = 0.0    # Proprioception

    # ── Phase 3 — Core Cognition ──────────────────────────────────────────────
    H: float = 0.0          # EQ_EMOT_07 — Emotional state
    reward_signal: float = 0.0
    P_pred: float = 1.0     # EQ_PRED_08 — Prediction state
    pred_error: float = 1.0 # Prediction error
    C: float = 0.0          # EQ_CONS_10 — Consciousness
    object_perm: int = 0    # Object permanence stage 0-3
    ltm_events: int = 0     # Episodic memory count
    value: float = 0.0      # Value system V(s)
    attachment: float = 0.0 # Attachment drive

    # ── Phase 3 — Language ────────────────────────────────────────────────────
    L: float = 0.0          # EQ_LANG_12 — Language state
    vocab: int = 0          # Vocabulary count
    tom_stage: int = 1      # Theory of Mind stage 1-5

    # ── Phase 4 — Social Cognitive ────────────────────────────────────────────
    grounding: float = 0.0  # Language grounding G(word)
    scene_graph_nodes: int = 0
    social_pred: float = 0.0

    # ── Phase 5 — Cultural ────────────────────────────────────────────────────
    W_world: float = 0.0    # EQ_WRLD_11 — World state
    cultural_embedding: float = 0.0
    npc_bonds: Dict[str, float] = field(default_factory=lambda: {
        "lorraine": 0.95, "alexis": 0.70, "evelyn": 0.65, "james": 0.30
    })

    # ── Phase 6 — Identity ────────────────────────────────────────────────────
    identity_confidence: float = 0.0
    narrative_coherence: float = 0.0
    skill_vector: List[float] = field(default_factory=lambda: [0.1]*22)

    # ── Phase 7 — Wisdom ──────────────────────────────────────────────────────
    wisdom: float = 0.0     # EQ_WISDOM_18 — W(t)
    creativity: float = 0.0 # EQ_CREAT_17 — C_new(t)
    career: float = 0.0     # EQ_CAREER_19
    legacy: float = 0.0     # EQ_LEGACY_20

    # ── Learning Loop ─────────────────────────────────────────────────────────
    ll_phase: str = "Exposure"
    curiosity: float = 0.3

    # ── History (ring buffer, last 100 ticks) ─────────────────────────────────
    history: List[Dict[str, Any]] = field(default_factory=list)

    def snapshot(self) -> Dict[str, Any]:
        """Return a lightweight snapshot for history."""
        return {
            "tick": self.tick, "week": round(self.week, 1),
            "height": round(self.height, 1), "mass": round(self.mass, 2),
            "HR": round(self.HR, 1), "ATP": round(self.ATP, 3),
            "C": round(self.C, 3), "pred_error": round(self.pred_error, 3),
            "vocab": self.vocab, "wisdom": round(self.wisdom, 3),
            "ltm": self.ltm_events, "motor": self.motor_stage,
            "tom": self.tom_stage, "ll_phase": self.ll_phase,
        }

    def life_stage(self) -> str:
        w = self.week
        if   w >= 1200: return "Mature Adult"
        elif w >= 1100: return "Mid Adult"
        elif w >= 1000: return "Adult"
        elif w >= 936:  return "Young Adult"
        elif w >= 624:  return "Adolescent"
        elif w >= 260:  return "Pre-Adolescent"
        elif w >= 156:  return "Child"
        elif w >= 80:   return "Toddler"
        elif w >= 52:   return "Infant"
        elif w >= 40:   return "Newborn"
        elif w >= 28:   return "Fetal Late"
        elif w >= 12:   return "Fetal Mid"
        elif w >= 4:    return "Fetal Early"
        else:           return "Embryo"