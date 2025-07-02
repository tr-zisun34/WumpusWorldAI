class KnowledgeBase:
    def __init__(self):
        self.facts = {}

    def tell(self, position, percepts):
        self.facts[position] = percepts

    def ask(self, position):
        return self.facts.get(position, {})

    def __str__(self):
        return "\n".join(f"{pos}: {percepts}" for pos, percepts in self.facts.items())
