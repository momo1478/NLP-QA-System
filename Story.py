class Story():
    def __init__(self):
        self.headline = ""
        self.date = ""
        self.id = ""
        self.words = []

    def __repr__(self):
        return " ".join(self.words)