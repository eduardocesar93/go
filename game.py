class Game:
    def __init__(self):
        self.black_ranking = -1
        self.white_ranking = -1
        self.result = 3
        self.valid = True
        self.komi = 0
        self.size = 19
        self.positions = list()

    def to_row(self):
        return [self.black_ranking, self.white_ranking, self.result, self.valid,
                self.komi, self.size, self.positions]
