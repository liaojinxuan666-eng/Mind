class Amygdala:
    def __init__(self):
        self.threats = {}
        self.rewards = {}

    def appraise(self, workspace):
        v = 0.0
        for item in workspace.spotlight:
            v += self.rewards.get(item.content, 0.0)
            v -= self.threats.get(item.content, 0.0)
        return v