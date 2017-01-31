class Game:
    def __init__(self):
        self.black_ranking = None
        self.white_ranking = None
        self.result = None
        self.valid = True
        self.komi = None
        self.size = 19
        self.positions = list()

    def to_row(self):
        return [self.black_ranking, self.white_ranking, self.result, self.valid,
                self.komi, self.size, self.positions]
