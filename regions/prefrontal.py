class PrefrontalCortex:
    def __init__(self, capacity=7):
        self.capacity = capacity
        self.working_memory = {}
        self.goal_stack = []

    def maintain(self, items):
        for i in items:
            if i.id in self.working_memory:
                old = self.working_memory[i.id]
                old.salience = max(old.salience, i.salience)
                old.last_active = i.last_active
            else:
                self.working_memory[i.id] = i

        if len(self.working_memory) > self.capacity:
            ordered = sorted(
                self.working_memory.values(),
                key=lambda x: (x.salience, x.last_active),
                reverse=True,
            )
            self.working_memory = {i.id: i for i in ordered[:self.capacity]}

    def decay_all(self, rate=0.05):
        for i in self.working_memory.values():
            i.decay(rate)
        self.working_memory = {
            k: v for k, v in self.working_memory.items() if v.salience > 0.0
        }

    def snapshot(self):
        return list(self.working_memory.values())

    def set_goal(self, goal):
        if goal:
            self.goal_stack.append(goal)
            self.goal_stack = self.goal_stack[-3:]

    def current_goal(self):
        return self.goal_stack[-1] if self.goal_stack else ""