class Dashboard:
    """
    Read-only dashboard for introspection.
    Renders snapshot data for human inspection.
    """

    def __init__(self, snapshot):
        self.snapshot = snapshot

    def render_text(self) -> str:
        view = self.snapshot.capture()

        lines = []
        lines.append("=== WORLD ===")
        for k, v in view.get("world", {}).items():
            lines.append(f"{k}: {v}")

        lines.append("\n=== MEMORY (recent) ===")
        for e in view.get("memory", []):
            lines.append(str(e))

        lines.append("\n=== ATTENTION ===")
        for e in view.get("attention", []):
            lines.append(str(e))

        lines.append("\n=== PREDICTION ===")
        for k, v in view.get("prediction", {}).items():
            lines.append(f"{k}: {v}")

        lines.append("\n=== COUNCIL ===")
        for k, v in view.get("council", {}).items():
            lines.append(f"{k}: {v}")

        return "\n".join(lines)
