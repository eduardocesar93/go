RESULTS = {'black': 0, 'white': 1,'tie': 2, 'undefined': 3}

# util functions
def rank(rank_str):
    if len(rank_str) == 0:
        return -1 # error
    category = rank_str[-1]
    number_rank = int(rank_str[0:-1])
    if category == 'k' or category == 'K':
        return 31 - number_rank
    elif category == 'd' or category == 'D':
        return number_rank + 30
    elif category == 'p' or category == 'P':
        return number_rank + 40
    else:
        return -1 # error

def convert_game(game_str):
    game = Game()
    char_buffer = ['', '', '']
    pointer = 0
    for i in range(len(game_str)):
        char_buffer[pointer] = game_str[i]
        char1 = char_buffer[(pointer - 2) % 3]
        char2 = char_buffer[(pointer - 1) % 3]
        char3 = char_buffer[pointer]
        if  char1 == ';' and (char2 == 'B' or char2 == 'b') and char3 == '[':
            game.positions.append(['b', ord(game_str[i + 1]) - ord('a'),
                ord(game_str[i + 2]) - ord('a')])
        elif char1 == ';' and (char2 == 'W' or char2 == 'w') and char3 == '[':
            game.positions.append(['w', ord(game_str[i + 1]) - ord('a'),
                ord(game_str[i + 2]) - ord('a')])
        elif char1 == 'S' and char2 == 'Z' and char3 == '[':
            j = i + 2
            while game_str[j] != ']':
                j += 1
            game.size = int(game_str[i + 1: j])
        elif char1 == 'K' and char2 == 'M' and char3 == '[':
            j = i + 2
            while game_str[j] != ']':
                j += 1
            game.komi = float(game_str[i + 1: j])
        elif char1 == 'W' and char2 == 'R' and char3 == '[':
            j = i + 2
            while game_str[j] != ']':
                j += 1
            game.white_ranking = rank(game_str[i + 1: j])
        elif char1 == 'B' and char2 == 'R' and char3 == '[':
            j = i + 2
            while game_str[j] != ']':
                j += 1
            game.black_ranking = rank(game_str[i + 1: j])
        elif char1 == 'R' and char2 == 'E' and char3 == '[':
            j = i + 2
            while game_str[j] != ']':
                j += 1
            result_game = game_str[i + 1: j]
            if result_game[0] == 'b' or result_game[0] == 'B':
                game.result = 0
            elif result_game[0] == 'w' or result_game[0] == 'W':
                game.result = 1
            elif result_game[0] == 't' or result_game[0] == 'T':
                game.result = 2
            else:
                game.result = 3
        pointer = (pointer + 1) % 3
    if len(game.positions) == 0:
        game.valid = False
    if game.size != 19:
        game.valid = False
    return game

class Game:
    def __init__(self):
        self.black_ranking = None
        self.white_ranking = None
        self.result = None
        self.valid = True
        self.komi = None
        self.size = 0
        self.positions = list()

    def to_row(self):
        return [self.black_ranking, self.white_ranking, self.result, self.valid,
                self.komi, self.size, self.positions]
