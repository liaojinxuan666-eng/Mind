class EntorhinalCortex:
    def __init__(self):
        self.entities = {}
        self.relations = []

    def bind(self, entities, relations):
        for e in entities:
            self.entities[e] = self.entities.get(e, 0) + 1
        self.relations.extend(relations)