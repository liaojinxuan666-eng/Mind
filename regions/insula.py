class Insula:
    def __init__(self):
        self.state = {}

    def sense(self, brain_state):
        self.state = {
            "energy": 1.0 - brain_state.drives.get("rest", 0.0),
            "uncertainty": brain_state.neuromod.get("norepinephrine", 0.5),
        }
        return self.state