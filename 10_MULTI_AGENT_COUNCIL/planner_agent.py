# planner_agent.py

class PlannerAgent:
    """
    Suggests possible action sequences.
    """

    def suggest(self, goal: str) -> dict:
        return {
            "goal": goal,
            "plans": []
        }
