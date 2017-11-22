import utils


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
        self.states.append([])
        for i in range(19):
            self.states[0].append(19 * [0])

    def to_row(self):
        positions = ''
        for pos_index in range(len(self.positions)):
            current_position = self.positions[pos_index]
            current_position_str = '{0}-{1}-{2}'.format(current_position[0],
                                                        current_position[1],
                                                        current_position[2])
            if pos_index != len(self.positions) - 1:
                current_position_str += '.'
            positions += current_position_str
        return [self.black_ranking, self.white_ranking, self.result,
                self.valid, self.komi, self.size, self.handicap,
                positions]

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
            if len(current_position) == 3:
                game.positions.append([current_position[0],
                                       int(current_position[1]),
                                       int(current_position[2])])
        game.states = list()
        game.states.append([])
        for i in range(19):
            game.states[0].append(19 * [0])
        return game

    def get_next_position(self, pos):
        next_position = self.states[len(self.states) - 1]
        number = 0
        matrix_position = utils.matrix_value(self.states[len(self.states) - 1],
                                             pos)
        if pos[0] == 'b':
            number = 1
        elif pos[0] == 'w':
            number = 2
        captures = update_positions(next_position, number, pos[1], pos[2])
        self.states.append(next_position)
        finish = False
        if len(self.states) == len(self.positions) + 1:
            finish = True
        return captures, finish, matrix_position


class Stats:
    def __init__(self):
        self.dynamic = {}
        self.game_length = 500 * [0]
        self.matrix_values = 3**9 * [0]
        self.win = [0, 0]
        self.errors = {'game length': 0, 'win': 0}
        self.captures = 500 * [0]
        self.times_capture = 500 * [0]
        self.transition_matrix = list()
        self.last_capture = -1
        self.last_position_matrix = -1
        for i in range(3 ** 9):
            self.transition_matrix.append(3 ** 9 * [0])

    def update_stats_dynamic(self, game, captures, matrix_value):
        position = len(game.states)
        if captures > 0:
            if self.last_capture == -1:
                self.last_capture = position
            else:
                self.times_capture[position - self.last_capture] += 1
                self.last_capture = position
        if self.last_position_matrix != -1 and matrix_value != -1:
            self.transition_matrix[self.last_position_matrix][
                matrix_value] += 1
        self.last_position_matrix = matrix_value
        if matrix_value != -1:
            self.matrix_values[matrix_value] += 1
        if position < 500:
            self.captures[position] += 1

    def update_stats_game(self, game):
        self.update_game_length(game)
        self.update_win(game)

    def update_game_length(self, game):
        length = len(game.positions)
        if 0 < length < 500:
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


def update_positions(positions, number, x, y):
    positions[x][y] = number
    visited = list()
    number_deleted = 0
    for i in range(19):
        visited.append(19 * [False])
    surrounded = list()
    for i in range(19):
        surrounded.append(19 * [False])
    if x > 0 and positions[x - 1][y] not in [number, 0]:
        visit(positions, surrounded, number, visited, x - 1, y)
        number_deleted += clean(positions, surrounded, visited)
    if x < 18 and positions[x + 1][y] not in [number, 0]:
        visit(positions, surrounded, number, visited, x + 1, y)
        number_deleted += clean(positions, surrounded, visited)
    if y > 0 and positions[x][y - 1] not in [number, 0]:
        visit(positions, surrounded, number, visited, x, y - 1)
        number_deleted += clean(positions, surrounded, visited)
    if y < 18 and positions[x][y + 1] not in [number, 0]:
        visit(positions, surrounded, number, visited, x, y + 1)
        number_deleted += clean(positions, surrounded, visited)
    return number_deleted


def visit(positions, surrounded, number, visited, x, y):
    if visited[x][y]:
        return True
    visited[x][y] = True
    surrounded_flag = True
    if x > 0 and positions[x - 1][y] == 0:
        return False
    elif x > 0 and positions[x - 1][y] != number:
        return_flag = visit(positions, surrounded, number, visited, x - 1, y)
        if not return_flag:
            return False
    if x < 18 and positions[x + 1][y] == 0:
        return False
    elif x < 18 and positions[x + 1][y] != number:
        return_flag = visit(positions, surrounded, number, visited, x + 1, y)
        if not return_flag:
            return False
    if y > 0 and positions[x][y - 1] == 0:
        return False
    elif y > 0 and positions[x][y - 1] != number:
        return_flag = visit(positions, surrounded, number, visited, x, y - 1)
        if not return_flag:
            return False
    if y < 18 and positions[x][y + 1] == 0:
        return False
    elif y < 18 and positions[x][y + 1] != number:
        return_flag = visit(positions, surrounded, number, visited, x, y + 1)
        if not return_flag:
            return False
    surrounded[x][y] = surrounded_flag
    return True


def clean(positions, surrounded, visited):
    delete = True
    number_deleted = 0
    for i in range(19):
        for j in range(19):
            if visited[i][j] != surrounded[i][j]:
                delete = False
                break
    if delete:
        for i in range(19):
            for j in range(19):
                if visited[i][j]:
                    number_deleted += 1
                    positions[i][j] = 0
                    visited[i][j] = False
                    surrounded[i][j] = False
    else:
        for i in range(19):
            for j in range(19):
                visited[i][j] = False
                surrounded[i][j] = False
    return number_deleted


def is_surrounded(surrounded, visited):
    delete = True
    for i in range(19):
        for j in range(19):
            if visited[i][j] != surrounded[i][j]:
                delete = False
                break
    if delete:
        return True
    else:
        return False


def nesting_two(row_1, row_2, lim):
    count_row_1 = 0
    count_row_2 = 0
    inter_count = 0
    for index in range(lim):
        if row_1[index] > 0:
            count_row_1 += 1
        if row_2[index] > 0:
            count_row_2 += 1
        if row_1[index] > 0 and row_2[index] > 0:
            inter_count += 1
    if count_row_1 == 0 or count_row_2 == 0:
        return 0
    if count_row_1 < count_row_2:
        return inter_count / count_row_1
    else:
        return inter_count / count_row_2


def nesting(matrix, lim):
    average_nesting = 0
    for i in range(lim):
        for j in range(lim):
            average_nesting += nesting_two(matrix[i], matrix[j], lim)
    return average_nesting / (lim * lim)
