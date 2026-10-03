class AnteriorCingulate:
    def __init__(self):
        self.conflict = 0.0
        self.errors = []

    def monitor(self, candidates, prediction_error):
        self.conflict = 0.0
        if len(candidates) > 1:
            vals = [c["value"] for c in candidates]
            if max(vals) - min(vals) < 0.1:
                self.conflict = 1.0
        if prediction_error > 0.5:
            self.errors.append(prediction_error)
        return self.conflict