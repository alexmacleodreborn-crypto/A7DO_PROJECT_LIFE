# causality/forward_only.py

class ForwardCausality:
    """
    Prevents backward causation.
    """

    def validate(self, t_now, t_next):
        if t_next <= t_now:
            raise RuntimeError("Causality violation: time reversal")
