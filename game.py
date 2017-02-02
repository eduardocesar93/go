class Game:
    def __init__(self):
        self.black_ranking = -1
        self.white_ranking = -1
        self.result = 3
        self.valid = True
        self.komi = 0
        self.size = 19
        self.handicap = 0
        self.positions = list()
        self.states = list()

    def to_row(self):
        return [self.black_ranking, self.white_ranking, self.result, self.valid,
                self.komi, self.size, self.handicap, self.positions]


class Stats:
    def __init__(self):
        self.dynamic = {}
        self.game = {}

    def update_stats_dynamic(self, game):
        # TODO
        return False

    def update_stats_game(self, game):
        # TODO
        return False
