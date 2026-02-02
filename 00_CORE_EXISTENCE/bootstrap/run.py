# bootstrap/run.py

from bootstrap.seed_init import initialize_seed

def run():
    core = initialize_seed()
    print("A7DO initialized")
    print(core["identity"].as_dict())

if __name__ == "__main__":
    run()
