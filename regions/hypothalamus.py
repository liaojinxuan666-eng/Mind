class Hypothalamus:
    def __init__(self):
        self.drives = {"curiosity": 0.5, "competence": 0.5, "safety": 1.0, "rest": 0.0}

    def update(self, tick):
        self.drives["rest"] = min(1.0, self.drives["rest"] + 0.001 * tick)
        self.drives["curiosity"] = max(0.0, self.drives["curiosity"] - 0.0005 * tick)

    def dominant(self):
        return max(self.drives, key=self.drives.get)