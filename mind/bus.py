from collections import defaultdict

class WhiteMatter:
    def __init__(self):
        self.subs = defaultdict(list)
        self.trace = []

    def subscribe(self, topic, fn):
        self.subs[topic].append(fn)

    def publish(self, topic, payload):
        self.trace.append((topic, payload))
        for fn in self.subs[topic]:
            fn(payload)