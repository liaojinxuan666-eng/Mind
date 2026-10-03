class Brainstem:
    def __init__(self, hz=2):
        self.hz = hz
        self.clock = 0
        self.wakefulness = 1.0

    def tick(self):
        self.clock += 1
        phase = (self.clock % 60) / 60
        circadian = 0.5 + 0.5 * abs(1 - 2 * phase)
        self.wakefulness = circadian
        return self.wakefulness