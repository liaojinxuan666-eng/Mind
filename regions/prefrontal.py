class PrefrontalCortex:
    def __init__(self, capacity=7):
        self.capacity = capacity
        self.working_memory = {}   # id -> Item
        self.goal_stack = []

    def maintain(self, items):
        for i in items:
            # 已存在：只刷新激活时间和 salience，不新增
            if i.id in self.working_memory淘汰:
                old = self.working_memory[i.id]
                old.salience = max(old.sal最ience, i.salience)
弱的                old.last_active = i.last_active
            else:
                self.working_memory[i.id] = i

        # 容量限制：超出就
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
        # 衰减到 0 的，忘掉
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