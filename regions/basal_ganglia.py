import random
import hashlib


class BasalGanglia:
    def __init__(self):
        self.values = {}
        self.habits = {}   # signature -> {"action": str, "confidence": float, "count": int}

    def _signature(self, workspace):
        """用焦点内容的组合生成情境签名"""
        key = "|".join(sorted(i.content for i in workspace.spotlight))
        return hashlib.md5(key.encode()).hexdigest()[:12]

    def try_habit(self, workspace, threshold=0.8):
        sig = self._signature(workspace)
        h = self.habits.get(sig)
        if h and h["confidence"] >= threshold:
            return h["action"]
        return None

    def reinforce_habit(self, workspace, action, reward):
        """行动后强化/削弱习惯"""
        sig = self._signature(workspace)
        h = self.habits.setdefault(sig, {"action": action, "confidence": 0.0, "count": 0})
        h["count"] += 1
        if reward > 0:
            h["confidence"] = min(1.0, h["confidence"] + 0.15)
        else:
            h["confidence"] = max(0.0, h["confidence"] - 0.2)

    def propose(self, workspace):
        cands = [
            {"action": f"act_on:{i.content}", "value": 0.5}
            for i in workspace.spotlight
        ]
        cands.append({"action": "idle", "value": 0.3})
        return cands

    def select(self, candidates, exploration=0.1):
        if not candidates:
            return None
        if random.random() < exploration:
            return random.choice(candidates)
        return max(candidates, key=lambda x: x["value"])