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

    @staticmethod
    def row_to_game(row):
        game = Game()
        game.black_ranking = int(row[0])
        game.white_ranking = int(row[1])
        game.result = int(row[2])
        game.valid = bool(row[3])
        game.komi = float(row[4])
        game.size = int(row[5])
        game.handicap = int(row[6])
        game.positions = list(row[7])
        game.states = list()


class Stats:
    def __init__(self):
        self.dynamic = {}
        self.game = {'game length': 500 * [0],
                     'win': [0, 0]
                     }
        self.errors = {'game length': 0, 'win': 0}

    def update_stats_dynamic(self, game):
        # TODO
        return False

    def update_stats_game(self, game):
        self.game_length(self, game)
        self.win(self, game)

    def game_length(self, game):
        length = len(game.positions)
        if length > 0:
            self.game['game length'][length] += 1
        else:
            self.errors['game length'] += 1

    def win(self, game):
        result = game.result
        if result == 0:
            self.game['win'][0] += 1
        elif result == 1:
            self.game['white'][1] += 1
        else:
            self.errors['win'] += 1
