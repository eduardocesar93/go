import game

RESULTS = {'black': 0, 'white': 1,'tie': 2, 'undefined': 3}


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
    if word == ';b[' or word == ';B[':
        game_instance.positions.append(['b', ord(game_str[position + 1]) - ord('a'),
                                        ord(game_str[position + 2]) - ord('a')])
    elif word == ';w[' or word == ';W[':
        game_instance.positions.append(['w', ord(game_str[position + 1]) - ord('a'),
                                        ord(game_str[position + 2]) - ord('a')])
    elif word in ['SZ[', 'KM[', 'WR[', 'BR[', 'RE[']:
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
            elif word == 'RE[':
                if content[0] == 'b' or content[0] == 'B':
                    game_instance.result = 0
                elif content[0] == 'w' or content[0] == 'W':
                    game_instance.result = 1
                elif content[0] == 't' or content[0] == 'T':
                    game_instance.result = 2
                else:
                    game_instance.result = 3


def convert_game(game_str):
    game_instance = game.Game()
    char_buffer = ['', '', '']
    pointer = 0
    for i in range(len(game_str)):
        char_buffer[pointer] = game_str[i]
        read_and_fill(game_instance, i, char_buffer, game_str, pointer)
        pointer = (pointer + 1) % 3
    if len(game_instance.positions) == 0:
        game_instance.valid = False
    if game_instance.size != 19:
        game_instance.valid = False
    return game_instance