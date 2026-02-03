from 12_INTERFACE_AND_OBSERVABILITY.visualisation import WebDashboard
from 12_INTERFACE_AND_OBSERVABILITY.snapshot import IntrospectionSnapshot

from 09_WORLD_MODEL.world_state import WorldState
from 07_MEMORY_SYSTEM.episodic import EpisodicMemory
from 06_LIMBIC_AND_VALUE_SYSTEM.attention import AttentionSystem
from 09_WORLD_MODEL.prediction import Predictor
from 10_MULTI_AGENT_COUNCIL.council import Council


def build_system():
    world = WorldState()
    memory = EpisodicMemory(capacity=20)
    attention = AttentionSystem(memory, focus_size=5)
    predictor = Predictor(world, memory)
    council = Council(world, memory, predictor, attention)

    # Seed with something visible
    memory.record({"type": "pain_withdrawal", "strain": 0.9}, salience=0.8)
    world.update(energy=4.0, strain=0.7)

    snapshot = IntrospectionSnapshot(
        world, memory, attention, predictor, council
    )
    return snapshot


if __name__ == "__main__":
    snapshot = build_system()
    WebDashboard(snapshot).run()
