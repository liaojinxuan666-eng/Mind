class Cerebellum:
    def __init__(self):
        self.last_prediction = None
        self.skills = {}

    def predict(self, action):
        self.last_prediction = self.skills.get(action, 0.5)
        return self.last_prediction

    def correct(self, actual):
        if self.last_prediction is None:
            return 0.0
        return actual - self.last_prediction