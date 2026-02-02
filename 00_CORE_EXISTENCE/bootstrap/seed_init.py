# bootstrap/seed_init.py

from identity.self_id import SelfIdentity
from heartbeat.clock import SystemClock
from heartbeat.pulse import Pulse

def initialize_seed():
    identity = SelfIdentity()
    clock = SystemClock()
    pulse = Pulse()

    return {
        "identity": identity,
        "clock": clock,
        "pulse": pulse
    }
