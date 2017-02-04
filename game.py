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
        positions = ''
        for pos_index in range(len(self.positions)):
            current_position = self.positions[pos_index]
            current_position_str = '{0}-{1}-{2}'.format(current_position[0], current_position[1], current_position[2])
            if pos_index != len(self.positions) - 1:
                current_position_str += '.'
            positions += current_position_str
        return [self.black_ranking, self.white_ranking, self.result, self.valid,
                self.komi, self.size, self.handicap, positions]

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
        game.positions = list()
        positions = row[7].split('.')
        for current_position_str in positions:
            current_position = current_position_str.split('-')
            game.positions.append([current_position[0], int(current_position[1]), int(current_position[2])])
        game.states = list()
        return game


class Stats:
    def __init__(self):
        self.dynamic = {}
        self.game_length = 500 * [0]
        self.win = [0, 0]
        self.errors = {'game length': 0, 'win': 0}

    def update_stats_dynamic(self, game):
        # TODO
        return False

    def update_stats_game(self, game):
        self.update_game_length(game)
        self.update_win(game)

    def update_game_length(self, game):
        length = len(game.positions)
        if length > 0:
            self.game_length[length] += 1
        else:
            self.errors['game length'] += 1

    def update_win(self, game):
        result = game.result
        if result == 0:
            self.win[0] += 1
        elif result == 1:
            self.win[1] += 1
        else:
            self.errors['win'] += 1
