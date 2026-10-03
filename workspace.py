class GlobalWorkspace:
    def __init__(self, capacity=7):
        self.capacity = capacity
        self.spotlight = []
        self.goal = ""

    def bind(self, gated, working_memory, goal):
        # 按 id 去重，保留 salience 最高的那个
        pool = {}
        for item in list(gated) + list(working_memory):
            if item.id not in pool or item.salience > pool[item.id].salience:
                pool[item.id] = item

        merged = sorted(pool.values(), key=lambda x: x.salience, reverse=True)
        self.spotlight = merged[:self.capacity]
        self.goal = goal
        return self.spotlight

    def compile(self):
        return {
            "focus": [i.content for i in self.spotlight],
            "goal": self.goal,
        }