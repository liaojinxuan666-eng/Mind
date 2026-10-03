class Thalamus:
    def __init__(self, k=5):
        self.k = k

    def gate(self, inputs, goal):
        scored = []
        for item in inputs:
            score = item.salience
            if goal and goal in item.content:
                score += 0.5
            scored.append((score, item))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in scored[:self.k]]