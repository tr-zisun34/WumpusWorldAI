class Cell:
    def __init__(self, x, y, content='-'):
        self.x = x
        self.y = y
        self.content = content  # '-', 'P', 'W', 'G'
        self.visited = False
        self.safe = False
