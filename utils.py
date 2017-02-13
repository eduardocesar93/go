import game

RESULTS = {'black': 0, 'white': 1, 'tie': 2, 'undefined': 3}


def rank(rank_str):
    if len(rank_str) == 0:
        return -1
    category = rank_str[-1]
    number_rank = int(rank_str[0:-1])
    if category == 'k' or category == 'K':
        return 31 - number_rank
    elif category == 'd' or category == 'D':
        return number_rank + 30
    elif category == 'p' or category == 'P':
        return number_rank + 40
    else:
        return -1


def read_and_fill(game_instance, position, char_buffer, game_str, pointer):
    word = char_buffer[(pointer - 2) % 3] + char_buffer[(pointer - 1) % 3] + char_buffer[pointer]
    if word == ';B[':
        if game_str[position + 1] != ']':
            game_instance.positions.append(['b', ord(game_str[position + 1]) - ord('a'),
                                            ord(game_str[position + 2]) - ord('a')])
    elif word == ';W[':
        if game_str[position + 1] != ']':
            game_instance.positions.append(['w', ord(game_str[position + 1]) - ord('a'),
                                            ord(game_str[position + 2]) - ord('a')])
    elif word == 'AB[':
        initial_position = position
        while game_str[initial_position] == '[':
            game_instance.positions.append(['b', ord(game_str[initial_position + 1]) - ord('a'),
                                            ord(game_str[initial_position + 2]) - ord('a')])
            initial_position += 4
    elif word == 'AW[':
        initial_position = position
        while game_str[initial_position] == '[':
            game_instance.positions.append(['b', ord(game_str[initial_position + 1]) - ord('a'),
                                            ord(game_str[initial_position + 2]) - ord('a')])
            initial_position += 4
    elif word in ['SZ[', 'KM[', 'WR[', 'BR[', 'HA[', 'RE[']:
        limit_position = position + 2
        while game_str[limit_position] != ']':
            limit_position += 1
        content = game_str[position + 1: limit_position]
        if word == 'SZ[':
            game_instance.size = int(content)
        elif word == 'KM[':
            game_instance.komi = float(content)
        elif word == 'WR[':
            game_instance.white_ranking = rank(content)
        elif word == 'BR[':
            game_instance.black_ranking = rank(content)
        elif word == 'HA[':
            game_instance.handicap = int(content)
        elif word == 'RE[':
            if content[0] == 'b' or content[0] == 'B':
                game_instance.result = 0
            elif content[0] == 'w' or content[0] == 'W':
                game_instance.result = 1
            elif content[0] == 't' or content[0] == 'T':
                game_instance.result = 2
            else:
                game_instance.result = 3


def convert_game(game_str, filters=False):
    game_instance = game.Game()
    char_buffer = ['', '', '']
    pointer = 0
    for i in range(len(game_str)):
        char_buffer[pointer] = game_str[i]
        read_and_fill(game_instance, i, char_buffer, game_str, pointer)
        pointer = (pointer + 1) % 3
    if filters:
        if game_instance.size != 19:
            game_instance.valid = False
        elif len(game_instance.positions) > filters['positions']['max'] or \
                len(game_instance.positions) < filters['positions']['min']:
            game_instance.valid = False
        elif game_instance.white_ranking not in filters['rank'] or \
                game_instance.black_ranking not in filters['rank']:
            game_instance.valid = False
        elif game_instance.result not in filters['result']:
            game_instance.valid = False
        elif game_instance.komi > filters['komi']['max'] or \
                game_instance.komi < filters['komi']['min']:
            game_instance.valid = False
        elif game_instance.handicap > filters['handicap']['max'] or \
                game_instance.handicap < filters['handicap']['min']:
            game_instance.valid = False
    return game_instance

def matrix_value(state, pos):
    if pos[1] in [0, 18] or pos[2] in [0. 18]:
        return -1
    else:
        x = pos[1]
        y = pos[2]
        matrix = [[state[x - 1][y - 1], state[x - 1][y], state[x - 1][y + 1]],
                  [state[x][y - 1],     pos[0],          state[x][y + 1]],
                  [state[x + 1][y - 1], state[x + 1][y], state[x + 1][y + 1]]]

def metric_base_2(matrix):
