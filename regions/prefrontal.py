from collections import deque

class PrefrontalCortex:
    def __init__(self, capacity=7):
        self.capacity = capacity
        self.working_memory = deque(maxlen=capacity)
        self.goal_stack = []

    def maintain(self, items):
        for i in items:
            self.working_memory.append(i)

    def set_goal(self, goal):
        if goal:
            self.goal_stack.append(goal)
            self.goal_stack = self.goal_stack[-3:]

    def current_goal(self):
        return self.goal_stack[-1] if self.goal_stack else ""