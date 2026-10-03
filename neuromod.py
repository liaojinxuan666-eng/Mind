class Neuromodulators:
    def __init__(self):
        self.dopamine = 0.5
        self.serotonin = 0.5
        self.acetylcholine = 0.5
        self.norepinephrine = 0.5

    def broadcast(self):
        return {
            "dopamine": self.dopamine,
            "serotonin": self.serotonin,
            "acetylcholine": self.acetylcholine,
            "norepinephrine": self.norepinephrine,
        }

    def update(self, td_error=0.0, novelty=0.0, threat=0.0):
        self.dopamine = 0.9 * self.dopamine + 0.1 * td_error
        self.norepinephrine = 0.9 * self.norepinephrine + 0.1 * threat
        self.acetylcholine = 0.9 * self.acetylcholine + 0.1 * novelty
        self.serotonin = 0.99 * self.serotonin + 0.005