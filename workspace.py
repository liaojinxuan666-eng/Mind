class GlobalWorkspace:
    def __init__(self, capacity=7):
        self.capacity = capacity
        self.spotlight = []
        self.goal = ""

    def bind(self, gated, working_memory, goal):
        merged = list(gated) + list(working_memory)
        merged.sort(key=lambda x: x.salience, reverse=True)
        self.spotlight = merged[:self.capacity]
        self.goal = goal
        return self.spotlight

    def compile(self):
        return {
            "focus": [i.content for i in self.spotlight],
            "goal": self.goal,
        }