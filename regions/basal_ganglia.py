import random

class BasalGanglia:
    def __init__(self):
        self.values = {}

    def propose(self, workspace):
        cands = [{"action": f"act_on:{i.content}", "value": 0.5} for i in workspace.spotlight]
        cands.append({"action": "idle", "value": 0.3})
        return cands

    def select(self, candidates, exploration=0.1):
        if not candidates:
            return None
        if random.random() < exploration:
            return random.choice(candidates)
        return max(candidates, key=lambda x: x["value"])