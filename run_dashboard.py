import time
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def load_module(name: str, relative_path: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Load life loop
life_mod = load_module(
    "life_loop",
    "00_CORE_EXISTENCE/bootstrap/life_loop.py"
)

LifeLoop = life_mod.LifeLoop


def main():
    life = LifeLoop()

    print("A7DO dashboard started\n")

    while life.pulse.is_alive():
        life.tick()

        # Structured debug output
        dbg = life.debug_snapshot()

        print("---- TICK ----")
        print("Alive:", dbg["alive"], "Awake:", dbg["awake"])
        print("Energy:", dbg["energy"])
        print("Fatigue:", dbg["fatigue"])
        print("Emotion:", dbg["emotion"])
        print("Curiosity:", dbg["curiosity"])
        print("Motivation:", dbg["motivation"])
        print("Salience:", dbg["salience"])
        print("Focused:", dbg["focused"])
        print()

        time.sleep(0.25)


if __name__ == "__main__":
    main()
