class DefaultModeNetwork:
    def __init__(self):
        self.narrative = []
        self.self_model = {"identity": "初生的脑子", "goals": []}

    def reflect(self, recent_episodes):
        for ep in recent_episodes[:3]:
            self.narrative.append(f"我经历了：{ep[2]} → {ep[4]}")
        return self.narrative[-3:]